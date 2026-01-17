from typing import Optional
from pydantic import BaseModel


class Signup_Schema(BaseModel):
    name: str
    email: str
    username: str
    password: str
    profile_photo: Optional[str]
    user_history: list[str] = []
