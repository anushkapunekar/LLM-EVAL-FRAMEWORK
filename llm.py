def get_llm_response(question: str) -> str:
    responses = {
        "what is python?": "Python is a programming language used in AI and backend systems.",
        "what is rag?": "RAG stands for Retrieval Augmented Generation combining search with LLMs.",
        "what is fastapi?": "FastAPI is a modern framework for building APIs using Python."
    }

    return responses.get(question.lower(), "I am not sure about that.")
