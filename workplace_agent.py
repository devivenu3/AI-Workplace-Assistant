
import os
import faiss
import ollama
import json
from sentence_transformers import SentenceTransformer
from workplace_tools import (
    get_leave_balance,
    check_calendar,
    submit_leave_request,
    approve_leave_request
)

# 1. Load the embedding model
embedding_model = SentenceTransformer("all-MiniLM-L6-v2")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

INDEX_PATH = os.path.join(BASE_DIR, "policy_index.faiss")
METADATA_PATH = os.path.join(BASE_DIR, "policy_metadata.json")

print("Loading saved policy index...")

index = faiss.read_index(INDEX_PATH)

with open(METADATA_PATH, "r", encoding="utf-8") as file:
    metadata = json.load(file)

documents = metadata["chunks"]
file_names = metadata["source_names"]

print(f"Loaded {len(documents)} policy chunks.")
print("Saved policy index loaded successfully!")




def answer_policy_question(question):
    """Retrieve a relevant policy and ask Llama to answer."""
    question_embedding = embedding_model.encode([question])
    distances, indices = index.search(question_embedding, k=1)

    result_index = indices[0][0]
    context = documents[result_index]
    source = file_names[result_index]

    prompt = f"""
    You are an AI workplace assistant.
    Answer the user's question using only the policy context below.

    Policy context:
    {context}

    User question:
    {question}

    Instructions:
    - Give a direct, clear answer based on the policy.
    - Do not classify the question or return a category label.
    - Do not invent information that is not in the policy.
    - If the policy does not contain the answer, say so.
    """

    response = ollama.chat(
        model="llama3.2",
        messages=[{"role": "user", "content": prompt}]
    )

    return response.message.content, source



def run_agent(question):
    """Route questions to workplace tools or policy retrieval."""

    decision = ollama.chat(
        model="llama3.2",
        messages=[{
            "role": "user",
            "content": f"""
            
            Classify the user's request into exactly one category.

            Question: {question}

            Rules:
            - LEAVE_REQUEST: The user wants to apply for, request, or submit leave.
            - LEAVE_TOOL: The user wants to check an individual employee's remaining leave balance.
            - CALENDAR_TOOL: The user wants to check meetings or an employee's calendar.
            - POLICY_RAG: The user asks about company policies, rules, or general entitlements.

            Examples:
            - "Apply for leave on 2026-10-05 for EMP001" -> LEAVE_REQUEST
            - "How many leave days does EMP001 have remaining?" -> LEAVE_TOOL
            - "What meetings does EMP001 have on 2026-10-02?" -> CALENDAR_TOOL
            - "How many paid leave days do employees receive per year?" -> POLICY_RAG
            - "How many days can employees work from home?" -> POLICY_RAG

            Return only one label:
            LEAVE_REQUEST
            LEAVE_TOOL
            CALENDAR_TOOL
            POLICY_RAG

            """
        }]
    )

    route = decision.message.content.strip().upper()
    words = question.upper().replace("?", "").split()
    employee_ids = [
        word for word in words if word.startswith("EMP")
    ]

    # Route 1: Submit a leave request
    if "LEAVE_REQUEST" in route:
        if not employee_ids:
            return "Please include an employee ID, such as EMP001.", None

        employee_id = employee_ids[0]

        import re
        dates = re.findall(r"\d{4}-\d{2}-\d{2}", question)

        if not dates:
            return (
                "Please provide the leave date in YYYY-MM-DD format.",
                None
            )

        reason = input("Please enter the reason for leave: ").strip()

        if not reason:
            return "A leave reason is required. No request was created.", None

        result = submit_leave_request(employee_id, dates[0], reason)

        if not result["success"]:
            return result["message"], None

        print("\nLeave request details:")
        print(f"Employee: {employee_id}")
        print(f"Date: {dates[0]}")
        print(f"Reason: {reason}")
        print("Status: PENDING_APPROVAL")

        approval = input(
            "\nDo you approve submitting this request? Type yes or no: "
        ).strip().lower()

        if approval == "yes":
            # The request was added at the end of the shared list.
            from workplace_tools import leave_requests
            request_index = len(leave_requests) - 1
            result = approve_leave_request(request_index)
            return result, "Mock leave-request records"

        return (
            "Request not approved. Its status remains pending in this session.",
            "Mock leave-request records"
        )

    # Route 2: Check leave balance
    elif "LEAVE_TOOL" in route:
        if not employee_ids:
            return "Please include an employee ID, such as EMP001.", None

        result = get_leave_balance(employee_ids[0])
        return result, "Employee records (mock data)"

    # Route 3: Check calendar
    elif "CALENDAR_TOOL" in route:
        if not employee_ids:
            return "Please include an employee ID, such as EMP001.", None

        import re
        dates = re.findall(r"\d{4}-\d{2}-\d{2}", question)

        if not dates:
            return (
                "Please provide a date in YYYY-MM-DD format, "
                "for example 2026-10-02.",
                None
            )

        result = check_calendar(employee_ids[0], dates[0])
        return result, "Calendar records (mock data)"

    # Route 4: Policy questions
    else:
        return answer_policy_question(question)

if __name__ == "__main__":
    print("AI Workplace Assistant")
    print("Type 'exit' to quit.\n")

    while True:
        question = input("You: ").strip()

        if question.lower() == "exit":
            print("Goodbye!")
            break

        if not question:
            continue

        try:
            answer, source = run_agent(question)
            print(f"\nAssistant: {answer}")

            if source:
                print(f"Source: {source}")

            print()
        except Exception as error:
            print("Something went wrong:", error)
