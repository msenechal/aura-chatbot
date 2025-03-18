from fastapi import HTTPException, Request
from question import Question
from config import ALLOWED_ORIGINS

class Routes:
    def __init__(self, app, rag, message_history):
        self._app = app
        self._rag = rag
        self._message_history = message_history
        self._register_routes()

    def register_routes(self):
        @self._app.post("/ask")
        def ask_question(request: Request, question: Question):
            try:
                referer = request.headers.get("referer", "")
                if not any(allowed in referer for allowed in ALLOWED_ORIGINS):
                    raise HTTPException(status_code=403, detail="Forbidden: Invalid referrer")
                
                history, _, current_session_id = self._message_history.create_message_history(session_id=question.session_id)

                input = question.question
                response = self._rag.search(
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