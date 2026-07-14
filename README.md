# 🤖 AI Candidate Digital Twin

An AI-powered Candidate Digital Twin that allows recruiters to interact with a candidate using natural language. Recruiters can upload a candidate's resume and ask questions about skills, education, projects, certifications, and experience.

---

## 🚀 Features

- 📄 Upload PDF, DOCX and TXT resumes
- 🔍 Automatic document parsing
- 🧠 AI-powered question answering
- 📚 Retrieval-Augmented Generation (RAG)
- 💾 ChromaDB vector database
- 🤖 LangGraph AI Agent
- ⚡ Groq LLM integration
- 🎨 Modern React + TypeScript frontend
- 🚀 FastAPI backend
- 👤 Single active candidate profile

---

# 🏗️ Tech Stack

### Frontend

- React
- TypeScript
- Vite
- CSS

### Backend

- FastAPI
- LangGraph
- ChromaDB
- Sentence Transformers
- Groq API
- Python

---

# 📂 Project Structure

```
AI-Digital-Twin/
│
├── backend/
│   ├── app/
│   ├── requirements.txt
│
├── frontend/
│   ├── src/
│   ├── public/
│
└── README.md
```

---

# ⚙️ Installation

## Clone Repository

```bash
git clone https://github.com/sangadhruva/AI-Digital-Twin.git

cd AI-Digital-Twin
```

---

## Backend

```bash
cd backend

pip install -r requirements.txt

uvicorn app.main:app --reload
```

Backend runs at

```
http://localhost:8001
```

Swagger API

```
http://localhost:8001/docs
```

---

## Frontend

```bash
cd frontend

npm install

npm run dev
```

Frontend runs at

```
http://localhost:5173
```

---

# 💡 How It Works

1. Upload a candidate resume.
2. The backend extracts text.
3. Text is split into chunks.
4. Chunks are stored in ChromaDB.
5. Recruiters ask questions.
6. Relevant chunks are retrieved.
7. LangGraph orchestrates the workflow.
8. Groq LLM generates the final answer.

---

# 📸 Screenshots

Add screenshots here.

Example:

- Home Page
- Resume Upload
- AI Chat
- Question Answering

---

# 🔮 Future Improvements

- Recruiter Dashboard
- Multiple Candidate Profiles
- Authentication
- Cloud Deployment
- Voice Interaction
- Interview Report Generation

---

# 👨‍💻 Author

**Sanga Dhruva**

GitHub

https://github.com/sangadhruva

LinkedIn

https://www.linkedin.com/in/sanga-dhruva-688287322/

---

# ⭐ If you found this project useful, consider giving it a star.