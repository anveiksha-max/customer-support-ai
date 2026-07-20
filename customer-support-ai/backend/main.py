import uuid
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from backend import database
from backend.agents.router import route_query
from backend.api.auth_routes import router as auth_router
from backend.api.analytics_routes import router as analytics_router
from backend.auth import get_current_user

app = FastAPI(title="TechMart Multi-Agent AI Customer Support")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(analytics_router)


class ChatRequest(BaseModel):
    session_id: str | None = None
    message: str


class ChatResponse(BaseModel):
    session_id: str
    answer: str
    agents_used: list[str]
    intents: list[str]
    sources: list[str]
    escalated: bool


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/history/{session_id}")
def history(session_id: str, current_user: dict = Depends(get_current_user)):
    return {"session_id": session_id, "messages": database.get_history(session_id)}


@app.post("/chat", response_model=ChatResponse)
def chat(req: ChatRequest, current_user: dict = Depends(get_current_user)):
    session_id = req.session_id or str(uuid.uuid4())

    # Build short conversation history for context
    past = database.get_history(session_id, limit=10)
    history_text = "\n".join([f"{m['role']}: {m['content']}" for m in past]) if past else ""

    database.save_message(session_id, "user", req.message)

    result = route_query(req.message, history_text)

    database.save_message(
        session_id, "assistant", result["answer"], agent=",".join(result["agents_used"])
    )

    return ChatResponse(
        session_id=session_id,
        answer=result["answer"],
        agents_used=result["agents_used"],
        intents=result["intents"],
        sources=result["sources"],
        escalated=result["escalated"],
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("backend.main:app", host="0.0.0.0", port=8000, reload=True)
