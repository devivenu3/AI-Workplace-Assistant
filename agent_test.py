
import ollama
from workplace_tools import get_leave_balance

# Give the model access to our Python tool
messages = [
    {
        "role": "user",
        "content": "How many leave days does employee EMP001 have?"
    }
]

response = ollama.chat(
    model="llama3.2",
    messages=messages,
    tools=[get_leave_balance]
)

# Check whether the model requested a tool
messages.append(response.message)

if response.message.tool_calls:
    for tool_call in response.message.tool_calls:
        if tool_call.function.name == "get_leave_balance":
            result = get_leave_balance(
                **tool_call.function.arguments
            )

            print("Tool executed:", result)

            # Give the tool result back to the model
            messages.append({
                "role": "tool",
                "tool_name": "get_leave_balance",
                "content": str(result)
            })

    # Ask the model to explain the result
    final_response = ollama.chat(
        model="llama3.2",
        messages=messages,
        tools=[get_leave_balance]
    )

    print("\nAssistant:", final_response.message.content)

else:
    print("The model did not request a tool call.")
    print("Model response:", response.message.content)
