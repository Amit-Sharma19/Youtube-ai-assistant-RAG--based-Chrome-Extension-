from youtube_transcript_api import (
    YouTubeTranscriptApi,
    TranscriptsDisabled,
)

from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import (
    HuggingFaceEmbeddings,
    HuggingFaceEndpoint,
    ChatHuggingFace,
)
from langchain_community.vectorstores import FAISS

from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import (
    RunnableParallel,
    RunnablePassthrough,
    RunnableLambda,
)
from langchain_core.output_parsers import StrOutputParser

from dotenv import load_dotenv

load_dotenv()

# ==========================================================
# Models (Loaded Once)
# ==========================================================

splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200,
)

embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
)

# ----------------------------------------------------------
# LLM
# ----------------------------------------------------------

llm = HuggingFaceEndpoint(
    repo_id="meta-llama/Llama-3.1-8B-Instruct",
)

model = ChatHuggingFace(llm=llm)

parser = StrOutputParser()

# ==========================================================
# Prompt
# ==========================================================

prompt = PromptTemplate(
    template="""
You are an AI assistant that answers questions ONLY using the provided transcript context.

Rules:

1. Always answer in English.

2. The transcript may be written in any language.

3. Use only the transcript context.

4. Use previous conversation if it helps.

5. If the answer is not present in the transcript, reply exactly:

"I don't know based on the video's transcript."

Conversation History:

{history}

Relevant Transcript Chunks:

{context}

Question:

{question}

Answer:
""",
    input_variables=[
        "history",
        "context",
        "question",
    ],
)

# ==========================================================
# Memory
# ==========================================================

video_cache = {}

chat_history = {}

# ==========================================================
# Helper Functions
# ==========================================================


def format_docs(retrieved_docs):

    return "\n\n".join(
        doc.page_content
        for doc in retrieved_docs
    )


def get_history(video_id):

    return chat_history.get(video_id, [])


def add_to_history(video_id, role, message):

    if video_id not in chat_history:

        chat_history[video_id] = []

    chat_history[video_id].append(
        {
            "role": role,
            "message": message,
        }
    )


def clear_chat(video_id):

    if video_id in chat_history:

        del chat_history[video_id]


def clear_cache():

    video_cache.clear()


def cache_info():

    return {

        "cached_videos": len(video_cache),

        "video_ids": list(video_cache.keys()),

    }


# ==========================================================
# Retriever
# ==========================================================


def get_retriever(video_id):

    if video_id in video_cache:

        print(f"✅ Using cached retriever : {video_id}")

        return video_cache[video_id]

    print(f"📥 Creating retriever : {video_id}")

    try:

        transcript_list = YouTubeTranscriptApi().fetch(
            video_id,
            languages=[
                "en",
                "hi",
                "ta",
                "te",
                "ml",
                "kn",
                "mr",
                "bn",
                "gu",
                "pa",
                "ur",
                "es",
                "fr",
                "de",
                "ja",
                "ko",
                "zh-Hans"
            ]
        )

        transcript = " ".join(
            chunk.text
            for chunk in transcript_list
        )
       
    except TranscriptsDisabled:

        raise Exception(
            "Transcript is disabled."
        )

    except Exception as e:

        raise Exception(
            f"Transcript Error : {e}"
        )

    documents = splitter.create_documents(
        [transcript]
    )

    vector_store = FAISS.from_documents(
        documents,
        embeddings,
    )

    retriever = vector_store.as_retriever(
        search_type="similarity",
        search_kwargs={"k": 4},
    )

    video_cache[video_id] = retriever

    return retriever


# ==========================================================
# Main Function
# ==========================================================


def answer_question(video_id, question):

    try:

        retriever = get_retriever(video_id)

        history = get_history(video_id)

        history_text = ""

        for item in history:

            history_text += (
                f"{item['role']}: "
                f"{item['message']}\n"
            )

        parallel_chain = RunnableParallel(
            {
                "context":
                    retriever
                    | RunnableLambda(format_docs),

                "question":
                    RunnablePassthrough(),

                "history":
                    RunnableLambda(
                        lambda x: history_text
                    ),
            }
        )

        chain = (
            parallel_chain
            | prompt
            | model
            | parser
        )

        answer = chain.invoke(question)

        add_to_history(
            video_id,
            "User",
            question,
        )

        add_to_history(
            video_id,
            "Assistant",
            answer,
        )

        return answer

    except Exception as e:

        return f"Error : {str(e)}"


# ==========================================================
# Local Testing
# ==========================================================

if __name__ == "__main__":

    while True:

        print()

        video_id = input(
            "Video ID (q to quit): "
        )

        if video_id.lower() == "q":

            break

        while True:

            print()

            question = input(
                "Question (new to change video): "
            )

            if question.lower() == "new":

                break

            answer = answer_question(
                video_id,
                question,
            )

            print()

            print("=" * 60)

            print(answer)

            print("=" * 60)

            print()

            print(cache_info())