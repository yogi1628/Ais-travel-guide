from fastapi import FastAPI, APIRouter, UploadFile, File, Form
from app.mongo import Destinations
from app.models import output_items

router = APIRouter(prefix="/destinations", tags=["Destinations"])


@router.get("/")
async def get_all_destinations():
    res = Destinations.find()
    all_destination = output_items(res)
    return all_destination
