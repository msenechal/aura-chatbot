from fastapi import FastAPI,HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from chat_history import create_message_history
from config import ALLOWED_ORIGINS
from agent import create_rag

def create_api():

    app = FastAPI()

    app.add_middleware(
        CORSMiddleware,
        allow_origins=ALLOWED_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    rag = create_rag

    class Question(BaseModel):
        question: str
        session_id: str = None

    @app.post("/ask")
    def ask_question(request: Request, question: Question):
        try:
            referer = request.headers.get("referer", "")
            if not any(allowed in referer for allowed in ALLOWED_ORIGINS):
                raise HTTPException(status_code=403, detail="Forbidden: Invalid referrer")
            
            history, _, current_session_id = create_message_history(session_id=question.session_id)

            input = question.question
            response = rag.search(
                query_text=input, 
                retriever_config={"top_k": 10}, 
                return_context=True,
                message_history=history
            )
            
            history.add_message({"role": "user", "content": input})
            history.add_message({"role": "assistant", "content": response.answer})
            
            print(f"{question.question}")
            src = []
            for item in response.retriever_result.items:
                src.append(item.metadata)
                
            return {"response": response.answer, "src": src, "session_id": current_session_id}
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
        
    return app