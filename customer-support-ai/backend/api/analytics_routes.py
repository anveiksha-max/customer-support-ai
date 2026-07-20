# feedback + analytics endpoints

from fastapi import APIRouter, Depends

from backend.models.feedback import FeedbackRequest
from backend import database
from backend.auth import get_current_user

router = APIRouter(tags=["analytics"])


@router.post("/feedback")
def submit_feedback(req: FeedbackRequest, current_user: dict = Depends(get_current_user)):
    database.save_feedback(req.session_id, req.agent, req.rating)
    return {"status": "recorded"}


@router.get("/analytics")
def analytics(current_user: dict = Depends(get_current_user)):
    return database.get_analytics()
