from fastapi import APIRouter, Response, HTTPException, status, UploadFile, File, Depends, Form
from pydantic import BaseModel, EmailStr, Field
from models.users import User
from core.auth import create_access_token, create_refresh_token
from core.security import verify_password, hash_password
from core.apiresponse import ApiResponse 
from fastapi.responses import JSONResponse
import os, shutil
from utils.cloudinary import upload_on_cloudinary
from services.user_services import *
from core.apiresponse import ApiResponse

user_router = APIRouter(prefix="/api/v1/users", tags=["Users"])
# it is a standard practice to write routes like this 
# http:localhost:8000/api/v1/users

class LoginRequest(BaseModel):
    username : str = Field(...,min_length=3,max_length=30)
    email : EmailStr = Field(...)
    password : str

@user_router.post('/login')
async def login_user(login_data : LoginRequest,response:Response):
    # find user in DB
    user = await User.find_one(login_data.username==User.username)
    if not user:
        raise HTTPException(status_code=404,detail="User not found")
    
    # verify the password
    if not verify_password(login_data.password,user.password):
        raise HTTPException(status_code=401,detail="Invalid Credentials")
    
    # we are just providing user_id as payload of token
    token_payload = {"sub":str(user.id)}
    access_token = create_access_token(data=token_payload)
    refresh_token = create_refresh_token(data=token_payload)

    # save the refresh_token to the database here
    user.refresh_token = refresh_token
    await user.save(user)
    # This is the equivalent of Express: res.cookie('refreshToken', token, { httpOnly: true, secure: true })
    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,  # Crucial: Prevents JavaScript from reading the cookie
        secure=True,    # Crucial: Ensures cookie is only sent over HTTPS
        samesite="lax",
        max_age=7 * 24 * 60 * 60 # 7 days in seconds
    )

    # 5. Return the Access Token as a standard JSON response
    return {
        "message": "User logged in successfully",
        "access_token": access_token,
        "token_type": "bearer",
        "user": {
            "email": user.email,
            "username": user.username
        }
    }



class RegisterRequest(BaseModel):
    username: str = Field(..., min_length=3, max_length=30)
    email: EmailStr = Field(...)
    full_name: str = Field(..., min_length=3)
    password: str = Field(..., min_length=6)


@user_router.post("/register")
async def register_user(
    username: str = Form(...),
    email: EmailStr = Form(...),
    full_name: str = Form(...),
    password: str = Form(...),
    avatar: UploadFile = File(...),
):
    new_user = await register_user_service(
        username=username,
        email=email,
        full_name=full_name,
        avatar=avatar,
        password=password,
    )

    return ApiResponse(
        status_code=201,
        data={
            "username": new_user.username,
            "email": new_user.email,
            "full_name": new_user.full_name,
            "avatar": new_user.avatar,
        },
        message="User registered successfully",
    )
