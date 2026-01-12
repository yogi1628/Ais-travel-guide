from fastapi import FastAPI, APIRouter, UploadFile, File, Form
from dotenv import load_dotenv
import os
from pymongo import MongoClient
from bson.objectid import ObjectId
from fastapi.responses import FileResponse
import uuid
from app.routers import destinations_route, auth_route

load_dotenv()

app = FastAPI()

app.include_router(destinations_route.router)
app.include_router(auth_route.router)
