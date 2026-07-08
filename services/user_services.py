from fastapi import File, HTTPException, UploadFile
from models.users import User
from core.apierror import ApiError
from core.apiresponse import ApiResponse
import os,shutil
from utils.cloudinary import upload_on_cloudinary
from core.security import hash_password


def upload_avatar(avatar: UploadFile = File(...)):
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


async def register_user_service(
        username: str,
        email: str,
        full_name: str,
        avatar: UploadFile,
        password : str
):
    # get details from frontend
    # validation - non empty
    # Check if the user already exists
    # if exists raise exception
    # check for images and avatar 
    # uplaod them to cloudinary,avatar
    # remove password and refresh token from field response 
    # Check for user creation in DB 
    # return response
    existing_user = await User.find_one(
        {"$or": [{"username": username}, {"email": email}]}
    )

    if existing_user:
        raise ApiError(
            status_code=400,
            message="User with this username or email already exists",
            error=[{"username": username, "email": email}],
        )
    
    # Upload to cloudinary 
    try:
        avatar_upload_response = upload_avatar(avatar)
    except Exception as e:
        raise ApiError(
            status_code=500,
            message="Error uploading avatar",
            error=[{"error": str(e)}],
        )
    
    # create a new user instance 

    hashed_password = hash_password(password)
    new_user = User(
        username=username,
        email=email,
        full_name=full_name,
        avatar=avatar_upload_response.get("cloudinary_url"),
        cover_image=None,
        watch_history=[],
        password=hashed_password,
        refresh_token="",
    )
