from fastapi.security import OAuth2PasswordRequestForm
from fastapi import APIRouter, HTTPException, UploadFile, File, Form, Depends
import os
from app.auth import hash_password, verify_password, create_token, get_current_user
from app.mongo import Users
from app.models import Signup_Schema

router = APIRouter(prefix="/auth", tags=["Auth"])
Profile_photo_dir = "app/images/profile-photos"


@router.post("/signup")
async def signup(
    name: str = Form(...),
    email: str = Form(...),
    username: str = Form(...),
    password: str = Form(...),
    profile_photo: UploadFile = File(None),
):
    if Users.find_one({"username": username}):
        raise HTTPException(status_code=400, detail="User already exists")

    image_ext = profile_photo.filename.split(".")[-1]
    image_name = f"{username}.{image_ext}"
    image_path = os.path.join(Profile_photo_dir, image_name)
    user = Signup_Schema(
        name=name,
        email=email,
        username=username,
        password=hash_password(password),
        profile_photo=image_name,
    ).model_dump()

    with open(image_path, "wb") as f:
        f.write(await profile_photo.read())

    Users.insert_one(user)

    return {"message": "User created"}


# @router.post("/login")
# def login(username: str, password: str):
#     user = Users.find_one({"username": username})
#     if not user:
#         raise HTTPException(status_code=401, detail="Invalid credentials")

#     if not verify_password(password, user["password"]):
#         raise HTTPException(status_code=401, detail="Invalid credentials")

#     token = create_token({"sub": username})
#     return {"access_token": token, "token_type": "bearer"}


@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    username = form_data.username
    password = form_data.password

    user = Users.find_one({"username": username})
    if not user or not verify_password(password, user["password"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_token({"sub": username})
    return {"access_token": token, "token_type": "bearer"}


@router.get("/profile")
def profile(user=Depends(get_current_user)):
    return {"message": f"Welcome {user}"}


@router.post("/logout")
def logout():
    return {"message": "Just delete the token on frontend"}
