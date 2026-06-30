import jwt
import os 
from datetime import datetime , timezone,timedelta

ACCESS_SECRET_KEY = os.getenv("ACCESS_TOKEN_SECRET_KEY","super_fallback")
REFRESH_SECRET_KEY = os.getenv("REFRESH_TOKEN_SECRET_KEY","refresh_super_fallback")
ALGORITHM = "HS256"


ACCESS_TOKEN_EXPIRY = int(os.getenv("ACCESS_TOKEN_EXPIRY_MINUTES",15))
REFRESH_TOKEN_EXPIRY = int(os.getenv("REFRESH_TOKEN_EXPIRY_DAYS",7))

def create_access_token(data : dict) -> str:
    to_encode = data.copy()

    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRY)

    to_encode.update({"exp":expire})
    encoded_jwt = jwt.encode(to_encode,ACCESS_SECRET_KEY,algorithm=ALGORITHM)
    return encoded_jwt


def create_refresh_token(data : dict) -> str:
    to_encode = data.copy()

    expire = datetime.now(timezone.utc) + timedelta(days=REFRESH_TOKEN_EXPIRY)

    to_encode.update({"exp" : expire})

    encoded_jwt = jwt.encode(to_encode,REFRESH_SECRET_KEY,algorithm=ALGORITHM)
    return encoded_jwt
