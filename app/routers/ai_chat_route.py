from fastapi import APIRouter
import asyncio
from graph import responder

router = APIRouter(prefix="/chat", tags=["AI-Chat"])


@router.post("/{user_input}")
def ai_message(user_input: str):
    return asyncio.run(responder(user_input=user_input))
