import os 
from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie
from models.users import User
from constants import DB_NAME

async def connect_db():
    mongo_uri = os.getenv("MONGO_URI")
    
    try:
        # 1. Initialize the Motor Client (The Engine)
        client = AsyncIOMotorClient(mongo_uri)
        
        # 2. Force a connection to verify the server is alive
        await client.admin.command('ping')
        print("🏓 Ping successful! MongoDB is awake.")
        
        # 3. Select the database dynamically using dictionary syntax
        db = client[DB_NAME]
        
        # 4. Initialize Beanie (The ODM)
        await init_beanie(database=db, document_models=[User])
        
        print(f"⚙️ MongoDB connection to '{DB_NAME}' successful!")
        
    except Exception as e:
        print(f"❌ DATABASE CONNECTION FAILED: {e}")
        # In production, you might want to exit the app if the DB fails to connect
        raise e

