from fastapi import APIRouter, Response, HTTPException, status,UploadFile,File,Depends
from pydantic import BaseModel,EmailStr,Field
from models.users import User
from core.auth import create_access_token, create_refresh_token
from core.security import verify_password,hash_password
from core.apiresponse import ApiResponse 
from fastapi.responses import JSONResponse
import os,shutil
from utils.cloudinary import upload_on_cloudinary
from services.user_services import *

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


@user_router.post('/register/avatar')
async def upload_avatar(avatar: UploadFile = File(...)):
    if not avatar:
        raise HTTPException(status_code=400, detail="File must be an image")
    
    # temp storage
    temp_folder = "public/temp"
    os.makedirs(temp_folder,exist_ok=True)

    file_location = f"{temp_folder}/{avatar.filename}"
    # Upload 
    try:
        with open(file_location,"wb+") as file_obj:
            shutil.copyfileobj(avatar.file,file_obj)
    except Exception as e:
        raise HTTPException(status_code=500,detail="Could not upload File")
    finally:
        avatar.file.close()

    cloudinary_response = upload_on_cloudinary(file_location)

    if not cloudinary_response:
        raise HTTPException(status_code=500, detail="Error uploading file on cloudinary")

    # 3. Return the secure URL provided by Cloudinary
    return {
        "message": "Avatar uploaded successfully!", 
        "cloudinary_url": cloudinary_response.get("secure_url"),
        "original_filename": avatar.filename
    }


# @user_router.post('/register')
# async def register_user(user: User):
#     new_user = await register_user_service(user=user)
#     return {
#         "success" : True,
#         "message" : "User Registered successfully",
#         "data" : {
#             "username" : new_user.username,
#             "email" : new_user.email
#         }
#     }