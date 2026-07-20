from pydantic import BaseModel


class FeedbackRequest(BaseModel):
    session_id: str
    agent: str
    rating: str  # "up" or "down"
