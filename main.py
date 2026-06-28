from fastapi import FastAPI
from contextlib import asynccontextmanager
from dotenv import load_dotenv
from db.connect import connect_db
from router.users_router import router
from fastapi.middleware.cors import CORSMiddleware
# context manager helps to safely manage resources like database connection before starting and after cleanup without writing a class and also avoiding try/finally blocks

# load variables from .env

load_dotenv()


# lifespan runs function before server starts recieving requests and close after handling all requests hence it is called lifespan
@asynccontextmanager
async def lifespan(app: FastAPI):
    await connect_db()

    yield
    # anything below yield runs on closing
    print("Connection Closed")


app = FastAPI(lifespan=lifespan, title="YT_PROJECT_BACKEND")

app.include_router(router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"], # Your frontend URL
    allow_credentials=True,
    allow_methods=["*"], # Allows GET, POST, PUT, DELETE, etc.
    allow_headers=["*"], 
)

@app.get("/")
def root():
    return {"message": "Server and Database are live!"}
