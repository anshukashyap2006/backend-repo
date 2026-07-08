from beanie import Document,Indexed,Link,Insert,Replace,SaveChanges,before_event
from datetime import datetime,timezone
from pydantic import EmailStr,Field
from typing import Annotated,Optional
from core.security import hash_password,verify_password
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from models.video import Video  


class User(Document):
    username: Annotated[str,Indexed(unique=True),Field(...)]
    email: Annotated[EmailStr,Indexed(unique = True),Field(...)]
    full_name : Annotated[str,Indexed(unique=False),Field(...)]
    avatar: Optional[str] = Field(default=None)
    cover_image : Optional[str] = None
    watch_history: list[Link["Video"]] = Field(default_factory=list)
    password : Annotated[str,Field(...,description="Password is required")]
    refresh_token : str = Field(default="")
    created_at : datetime = Field(default_factory=lambda:datetime.now(timezone.utc))
    updated_at : datetime = Field(default_factory=lambda:datetime.now(timezone.utc))

    @before_event(Insert,Replace, SaveChanges)
    def update_timestamp(self):
        print("Updating the 'updated_at' timestamp...")
        self.updated_at = datetime.now(timezone.utc)

    @before_event(Insert,Replace)
    async def hash_password(self):
        # We only want to hash it if it's not already a bcrypt hash
        # (bcrypt hashes typically start with $2b$ or $2a$)
        if not self.password.startswith("$2"):
            self.password = hash_password(self.password)

            


    class Settings:
        name = "users"
        # indexes = [
        #     ([("username", 1)], {"unique": True}),
        # ]
        # This tells Beanie to name the MongoDB collection "users"