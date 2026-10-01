
from workplace_agent import answer_policy_question

# Test cases: question, expected policy source, expected keyword
test_cases = [
    {
        "question": "How many paid leave days do employees receive per year?",
        "expected_source": "leave_policy.txt",
        "expected_keyword": "18 days",
    },
    {
        "question": "How many days can employees work from home?",
        "expected_source": "remote_work.txt",
        "expected_keyword": "2 days",
    },
    {
        "question": "How far in advance should leave be requested?",
        "expected_source": "leave_policy.txt",
        "expected_keyword": "2 working days",
    },
    {
        "question": "Do remote work requests need manager approval?",
        "expected_source": "remote_work.txt",
        "expected_keyword": "manager approval",
    },
]

def evaluate_policy_retrieval():
    passed = 0

    print("\nAI Workplace Assistant - Policy Evaluation")
    print("=" * 50)

    for i, test in enumerate(test_cases, start=1):
        answer, source = answer_policy_question(test["question"])

        source_correct = source == test["expected_source"]
        answer_correct = (
            test["expected_keyword"].lower() in answer.lower()
        )

        success = source_correct and answer_correct

        if success:
            passed += 1

        print(f"\nTest {i}: {test['question']}")
        print(f"Expected source: {test['expected_source']}")
        print(f"Actual source:   {source}")
        print(f"Answer: {answer}")
        print(f"Result: {'PASS' if success else 'FAIL'}")

    total = len(test_cases)
    print("\n" + "=" * 50)
    print(f"Evaluation score: {passed}/{total}")
    print(f"Pass rate: {passed / total * 100:.1f}%")

if __name__ == "__main__":
    evaluate_policy_retrieval()
