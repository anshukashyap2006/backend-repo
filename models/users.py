from beanie import Document
from pydantic import EmailStr

class User(Document):
    username: str
    email: EmailStr
    password: str

    class Settings:
        name = "users" # This tells Beanie to name the MongoDB collection "users"