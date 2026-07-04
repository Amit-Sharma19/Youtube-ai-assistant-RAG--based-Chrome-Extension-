from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

from rag import answer_question

app = FastAPI(
    title="YouTube RAG API",
    version="1.0"
)

# Allow Chrome Extension to access the API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # We'll restrict this later
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --------------------------
# Request Model
# --------------------------

class QuestionRequest(BaseModel):
    video_id: str
    question: str


# --------------------------
# Health Check
# --------------------------

@app.get("/")
def home():
    return {
        "message": "YouTube RAG API is running!"
    }


# --------------------------
# Ask Endpoint
# --------------------------

@app.post("/ask")
def ask_question(request: QuestionRequest):

    answer = answer_question(
        request.video_id,
        request.question
    )

    return {
        "answer": answer
    }