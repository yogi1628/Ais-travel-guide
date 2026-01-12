from typing import Optional
from pydantic import BaseModel
from datetime import datetime


class Destination_Schema(BaseModel):
    name: str
    country: str
    type: str
    rating: float
    image: Optional[str] = None
    created_at: int = datetime.timestamp(datetime.now())
    updated_at: int = datetime.timestamp(datetime.now())
    deleted: bool = False


class Destination_update(BaseModel):
    name: Optional[str] = None
    country: Optional[str] = None
    type: Optional[str] = None
    rating: Optional[float] = None
    image: Optional[str] = None


class Signup_Schema(BaseModel):
    name: str
    email: str
    username: str
    password: str
    profile_photo: Optional[str]


def output_item(object):
    output = {
        "name": object["name"],
        "country": object["country"],
        "type": object["type"],
        "rating": object["rating"],
        "image": object["image"],
    }
    return output


def output_items(objects):
    output_list = [output_item(object) for object in objects]
    return output_list
