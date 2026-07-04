# 🎥 YouTube AI Assistant (Chrome Extension)

An AI-powered Chrome Extension that enables users to ask natural language questions about any YouTube video using Retrieval-Augmented Generation (RAG). The extension extracts the video's transcript, retrieves the most relevant information using vector search, and generates accurate context-aware answers with a Large Language Model.

---

## 🚀 Features

- 🎥 Ask questions directly from YouTube videos
- 🌍 Supports multilingual video transcripts
- 💬 Ask questions in English regardless of transcript language
- 🧠 Retrieval-Augmented Generation (RAG)
- 📄 Automatic transcript extraction using YouTube Transcript API
- 🔍 Semantic search using FAISS vector database
- 🤖 Context-aware responses using Llama 3.1
- 💾 Retriever caching for faster repeated queries
- 🗂️ Conversation history for follow-up questions
- ⚡ FastAPI backend with Chrome Extension frontend

---

## 🛠️ Tech Stack

### Frontend
- HTML
- CSS
- JavaScript
- Chrome Extension APIs

### Backend
- FastAPI
- LangChain
- FAISS
- Hugging Face Embeddings
- Hugging Face Inference API
- Llama 3.1
- YouTube Transcript API

---

## 📂 Project Structure

```
RAG/
│
├── backend/
│   ├── app.py
│   ├── rag.py
│   ├── requirements.txt
│   └── .env
│
├── extension/
│   ├── manifest.json
│   ├── sidepanel.html
│   ├── sidepanel.css
│   ├── sidepanel.js
│   ├── background.js
│   ├── content.js
│   └── icons/
│
└── README.md
```

---

## ⚙️ Installation

### 1. Clone the Repository

```bash
git clone https://github.com/YOUR_USERNAME/RAG-Youtube-AI-Assistant.git
```

```bash
cd RAG-Youtube-AI-Assistant
```

---

### 2. Create a Virtual Environment

```bash
python -m venv venv
```

Windows

```bash
venv\Scripts\activate
```

Linux/macOS

```bash
source venv/bin/activate
```

---

### 3. Install Dependencies

```bash
pip install -r backend/requirements.txt
```

---

### 4. Create a `.env` File

```env
HUGGINGFACEHUB_API_TOKEN=YOUR_HUGGINGFACE_API_KEY
```

---

### 5. Start the Backend

```bash
cd backend
```

```bash
uvicorn app:app --reload
```

Backend runs at:

```
http://127.0.0.1:8000
```

---

### 6. Load the Chrome Extension

1. Open Chrome
2. Go to **chrome://extensions/**
3. Enable **Developer Mode**
4. Click **Load unpacked**
5. Select the **extension** folder

---

## 🏗️ System Architecture

```
YouTube Video
      │
      ▼
Transcript Extraction
      │
      ▼
Text Chunking
      │
      ▼
Embedding Generation
      │
      ▼
FAISS Vector Store
      │
      ▼
Relevant Chunk Retrieval
      │
      ▼
Llama 3.1
      │
      ▼
Answer Generation
      │
      ▼
Chrome Extension UI
```


## 🔮 Future Improvements

- Voice-based questions
- PDF export of chat
- Streaming AI responses
- Multiple LLM support
- YouTube playlist support
- Cloud deployment
- User authentication

---

## 👨‍💻 Author

**Amit Sharma**

- GitHub: https://github.com/Amit-Sharma19


---

## ⭐ If you found this project useful, consider giving it a star!
