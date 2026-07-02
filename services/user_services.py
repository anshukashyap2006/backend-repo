from fastapi import HTTPException
from models.users import User


async def register_user_service(user: User):
    # Check if the user already exists
    existing_user = await User.find_one(User.username == user.username)
    if existing_user:
        raise HTTPException(status_code=409,detail="User Already exists")
    
    new_user = ""
    
    return new_user
