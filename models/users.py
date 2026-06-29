from beanie import Document,Indexed,Link,Insert,Replace,SaveChanges,before_event
from datetime import datetime,timezone
from pydantic import EmailStr,Field
from typing import Annotated,Optional
from models.video import Video

class User(Document):
    username: Annotated[str,Indexed(unique=True),Field(...)]
    email: Annotated[EmailStr,Indexed(unique = True),Field(...)]
    full_name : Annotated[str,Indexed(unique=False),Field(...)]
    avatar: str = Field(...)
    cover_image : Optional[str]
    watch_history : Link[Video]
    password : Annotated[str,Field(...,description="Password is required")]
    refresh_token : str
    created_at : datetime = Field(default_factory=lambda:datetime.now(timezone.utc))
    updated_at : datetime = Field(default_factory=lambda:datetime.now(timezone.utc))

    @before_event(Insert,Replace, SaveChanges)
    def update_timestamp(self):
        print("Updating the 'updated_at' timestamp...")
        self.updated_at = datetime.now(timezone.utc)

    class Settings:
        name = "users"
        # indexes = [
        #     ([("username", 1)], {"unique": True}),
        # ]
        # This tells Beanie to name the MongoDB collection "users"