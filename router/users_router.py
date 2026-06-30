from fastapi import APIRouter, Response, HTTPException, status
from pydantic import BaseModel,EmailStr,Field
from models.users import User
from src.core.auth import create_access_token, create_refresh_token
from src.core.security import verify_password,hash_password
from src.core.apiresponse import ApiResponse 

router = APIRouter(prefix="/users", tags=["Users"])


class LoginRequest(BaseModel):
    email : EmailStr = Field(...)
    password : str

@router.post('/login')
async def login_user(login_data : LoginRequest,response:Response):
    # find user in DB
    user = await User.find_one(login_data.email==User.email)
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




