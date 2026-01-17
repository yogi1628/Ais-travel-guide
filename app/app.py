from fastapi import FastAPI
from dotenv import load_dotenv
from app.routers import auth_route, ai_chat_route

load_dotenv()

app = FastAPI()

app.include_router(auth_route.router)
app.include_router(ai_chat_route.router)
