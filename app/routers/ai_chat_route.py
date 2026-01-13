from fastapi import APIRouter, Depends, HTTPException, Form
import asyncio
from graph import responder
from app.auth import get_current_user

router = APIRouter(prefix="/chat", tags=["AI-Chat"])


@router.post("/chat")
async def ai_message(user_input: str, user=Depends(get_current_user)):
    ai_reply = await responder(user_input=user_input)
    return {"user": user, "message": ai_reply}
