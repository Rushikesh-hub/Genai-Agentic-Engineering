# 🚀 Agentic AI System with RAG, Multi-Agent Orchestration & Streaming UI

## 🔥 Overview
A production-grade AI system combining:
- Retrieval-Augmented Generation (RAG)
- Agentic AI (tool-using agents)
- Multi-agent collaboration
- Long-term memory
- Streaming responses
- FastAPI backend + Streamlit frontend

---

## 🧠 Features

- 🔍 RAG-based knowledge retrieval
- 🤖 Tool-using AI agents (search, calculator)
- 🧩 Multi-agent system (researcher, analyst, writer)
- 🧠 Vector-based memory
- ⚡ Streaming responses (real-time UX)
- 🧪 AI evaluation (quality scoring + hallucination detection)
- 🚀 FastAPI production backend
- 🐳 Dockerized deployment
- 🔐 API security + rate limiting
- 💬 ChatGPT-like UI

---

## 🏗 Architecture

User → UI → FastAPI → Agent System  
→ (RAG + Tools + Memory + Routing) → Response  

---

## 🛠 Tech Stack

- Python, FastAPI
- LangChain
- FAISS
- OpenAI API
- Streamlit
- Docker

---

## ▶️ Run Locally

```bash
git clone <repo>
cd project

pip install -r requirements.txt
uvicorn api.server:app --reload
streamlit run ui/app.py

