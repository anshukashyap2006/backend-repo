from beanie import Document,Indexed,Link,Insert,Replace,SaveChanges,before_event
from datetime import datetime,timezone
from pydantic import EmailStr,Field
from typing import Annotated,Optional
from models.users import User


class Video(Document):
    video_file: str = Field(...) #cloudnary url
    thumbnail : str = Field(...)
    title : str = Field(...)
    description : str = Field(...)
    duration : int = Field(...) # cloudnary url
    views : int = Field(default=0)
    is_published : bool = Field(default=True)
    owner : Link[User]
    created_at : datetime = Field(default_factory=lambda:datetime.now(timezone.utc))
    updated_at : datetime = Field(default_factory=lambda:datetime.now(timezone.utc))

    @before_event(Insert,Replace, SaveChanges)
    def update_timestamp(self):
        print("Updating the 'updated_at' timestamp...")
        self.updated_at = datetime.now(timezone.utc) 