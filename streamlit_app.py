
import streamlit as st
from datetime import date

from workplace_agent import run_agent
from workplace_tools import (
    submit_leave_request,
    approve_leave_request,
    leave_requests,
)

st.set_page_config(
    page_title="AI Workplace Assistant",
    page_icon="🤖",
    layout="centered",
)

st.title("🤖 AI Workplace Assistant")
st.caption(
    "Ask company policy questions, check leave balances, "
    "or look up calendar meetings."
)

# Keep chat history across Streamlit reruns
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": (
                "Hi! I can answer policy questions, check leave "
                "balances, and look up calendar meetings. "
                "What would you like help with?"
            ),
        }
    ]

# Display previous messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
if question := st.chat_input("Ask your workplace assistant..."):
    st.session_state.messages.append(
        {"role": "user", "content": question}
    )

    with st.chat_message("user"):
        st.markdown(question)

    # Leave requests need the dedicated approval form below.
    request_words = [
        "apply for leave",
        "request leave",
        "submit leave",
        "book leave",
    ]

    if any(phrase in question.lower() for phrase in request_words):
        answer = (
            "To request leave, please use the **Leave Request** "
            "form in the sidebar. This lets you review the details "
            "and approve the request explicitly."
        )
        source = None
    else:
        try:
            with st.spinner("Thinking..."):
                answer, source = run_agent(question)

            if source:
                answer += f"\n\n*Source: {source}*"

        except Exception as error:
            answer = f"Sorry, something went wrong: {error}"

    with st.chat_message("assistant"):
        st.markdown(answer)

    st.session_state.messages.append(
        {"role": "assistant", "content": answer}
    )

# Leave request form in the sidebar
with st.sidebar:
    st.header("Leave Request")
    st.caption("Demo only — uses fictional employee records.")

    with st.form("leave_request_form"):
        employee_id = st.selectbox(
            "Employee ID",
            ["EMP001", "EMP002"],
        )
        leave_date = st.date_input(
            "Leave date",
            min_value=date.today(),
        )
        reason = st.text_input("Reason for leave")

        submitted = st.form_submit_button("Prepare request")

    if submitted:
        if not reason.strip():
            st.error("Please enter a reason.")
        else:
            result = submit_leave_request(
                employee_id,
                leave_date.isoformat(),
                reason.strip(),
            )

            if result["success"]:
                st.session_state.pending_request_index = (
                    len(leave_requests) - 1
                )
                st.success("Request prepared for your review.")
            else:
                st.error(result["message"])

    # Explicit approval step
    if "pending_request_index" in st.session_state:
        request_index = st.session_state.pending_request_index

        if request_index < len(leave_requests):
            request = leave_requests[request_index]

            if request["status"] == "PENDING_APPROVAL":
                st.subheader("Review request")
                st.write(f"**Employee:** {request['employee_id']}")
                st.write(f"**Date:** {request['date']}")
                st.write(f"**Reason:** {request['reason']}")

                if st.button("Approve leave request"):
                    result = approve_leave_request(request_index)
                    st.success(result)
                    del st.session_state.pending_request_index

                if st.button("Cancel request"):
                    request["status"] = "CANCELLED"
                    st.info("Request cancelled.")
                    del st.session_state.pending_request_index
