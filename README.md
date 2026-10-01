
# AI Workplace Assistant & Automation Agent

An AI-powered workplace assistant that answers company policy questions and supports common HR workflows using retrieval-augmented generation (RAG), an LLM, and Python tools.

## Problem Statement

Employees often need to search through company policies or ask HR for routine information. This project demonstrates how an AI assistant can make internal information easier to access and help streamline simple workplace workflows.

## Features

- **Policy Q&A:** Answers questions using company policy documents.
- **Retrieval-Augmented Generation (RAG):** Uses Sentence Transformers and FAISS to retrieve relevant policy content before generating an answer.
- **Local LLM:** Uses Llama 3.2 through Ollama.
- **Workplace tools:** Demonstrates leave-balance lookup and calendar queries using mock employee records.
- **Leave requests:** Supports a mock leave-request workflow with approval.
- **Policy ingestion:** Builds and saves a FAISS index and policy metadata from text files.
- **Automated evaluation:** Tests policy retrieval sources and expected answer keywords.
- **Streamlit interface:** Provides a chat interface and mock leave-request form.

## Architecture

User → Streamlit UI / Terminal → Agent Routing → Policy RAG or Python Tools → Response

Policy RAG:
Policy documents → Embeddings → FAISS retrieval → Relevant context → Llama 3.2 → Answer

## Tech Stack

- Python
- Ollama
- Llama 3.2
- Sentence Transformers
- FAISS
- Streamlit
- Git and GitHub

## Project Structure

```text
AI-WORKPLACE-AGENT/
├── company_policies/
│   ├── leave_policy.txt
│   └── remote_work.txt
├── workplace_agent.py
├── workplace_tools.py
├── streamlit_app.py
├── ingestion_policies.py
├── evaluate_agent.py
├── test_agent.py
├── agent_test.py
├── ollama_test.py
└── .gitignore
```

## Setup

1. Install Python.
2. Install Ollama and download the model:

   `ollama pull llama3.2`

3. Install the Python dependencies:

   `pip install ollama sentence-transformers faiss-cpu streamlit`

4. Build the policy index:

   `python ingestion_policies.py`

5. Run the terminal assistant:

   `python workplace_agent.py`

6. Or run the Streamlit interface:

   `python -m streamlit run streamlit_app.py`

7. Run policy evaluation:

   `python evaluate_agent.py`

8. Run unit tests:

   `python -m unittest test_agent.py`

## Evaluation

The initial policy evaluation passed **4 out of 4 selected test cases (100%)**. The evaluation checks whether the expected policy source was retrieved and whether the answer contains a specified keyword. This is a small initial test set, not a guarantee of correctness for all questions.

## Limitations

- Employee records and calendar entries are mock data.
- Leave requests are stored in memory and are not connected to a real HR system.
- The local LLM requires Ollama to be installed and running.
- The current evaluation covers a small number of policy questions.

## Future Improvements

- Expand evaluation to cover routing, retrieval relevance, answer faithfulness, and failure cases.
- Add policy update monitoring and automatic index refresh.
- Integrate authentication and real enterprise systems.
- Add CI with GitHub Actions.
- Deploy the application for an accessible demo.
