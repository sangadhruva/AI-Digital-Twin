\# 🤖 Candidate Digital Twin



An AI-powered Candidate Digital Twin that allows recruiters to interact with a candidate's resume using natural language. Built using React, FastAPI, LangGraph, ChromaDB, and Groq LLM with Retrieval-Augmented Generation (RAG).



\---



\## 🚀 Features



\- 📄 Upload PDF, DOCX, and TXT resumes

\- 🧠 Automatic text extraction and chunking

\- 🔍 Semantic search using ChromaDB

\- 🤖 AI-powered recruiter assistant

\- 💬 Ask questions about:

&#x20; - Skills

&#x20; - Education

&#x20; - Experience

&#x20; - Projects

&#x20; - Certifications

\- ⚡ FastAPI REST backend

\- 🎨 Modern React + TypeScript frontend

\- 🔄 Single active candidate profile

\- 🗑 Clear candidate profile with one click



\---



\## 🏗 Tech Stack



\### Frontend

\- React

\- TypeScript

\- Vite

\- Axios

\- CSS



\### Backend

\- FastAPI

\- Python

\- LangGraph

\- Groq API

\- ChromaDB

\- Sentence Transformers

\- Uvicorn



\---



\## 📂 Project Structure



```

AI-Digital-Twin

│

├── backend

│   ├── app

│   │   ├── agents

│   │   ├── api

│   │   ├── rag

│   │   └── services

│   └── requirements.txt

│

├── frontend

│   ├── src

│   │   ├── components

│   │   ├── services

│   │   └── styles

│   └── package.json

│

└── README.md

```



\---



\## ⚙ Installation



\### Backend



```bash

cd backend

pip install -r requirements.txt

python -m uvicorn app.main:app --reload --port 8001

```



\### Frontend



```bash

cd frontend

npm install

npm run dev

```



\---



\## 🔄 Workflow



1\. Upload a resume

2\. Resume is parsed and cleaned

3\. Text is split into chunks

4\. Chunks are stored in ChromaDB

5\. Recruiter asks a question

6\. Relevant chunks are retrieved

7\. LangGraph agent generates the answer

8\. Response is displayed in the chat interface



\---



\## 📸 Screenshots



\### Home Page



\_Add screenshot here\_



\### Upload Resume



\_Add screenshot here\_



\### AI Chat



\_Add screenshot here\_



\---



\## 🔮 Future Improvements



\- Multi-candidate support

\- Voice interaction

\- Resume comparison

\- Interview simulation

\- Authentication

\- Cloud deployment

\- Conversation history



\---



\## 👨‍💻 Author



\*\*Sanga Dhruva\*\*



GitHub: https://github.com/sangadhruva



LinkedIn:

https://www.linkedin.com/in/sanga-dhruva-688287322/



\---



\## ⭐ If you like this project



Please consider giving it a ⭐ on GitHub.

