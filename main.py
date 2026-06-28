from fastapi import FastAPI,Request,Response
from contextlib import asynccontextmanager
from dotenv import load_dotenv
from db.connect import connect_db
from router.users_router import router
from fastapi.middleware.cors import CORSMiddleware

from fastapi.responses import JSONResponse
from core.apierror import ApiError


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

# Creating a global error handling middleware to ensure every single error sent back to the frontend has the exact same JSON structure (e.g., always returning { success: false, message: "...", statusCode: 400 }).
# This acts as a global net—if any route anywhere in the app raises an ApiError (which is our custom made class), this function intercepts it and formats the JSON response.
@app.exception_handler(ApiError)
async def api_error_handler(request: Request,exc: ApiError):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "success": exc.success,
            "message": exc.message,
            "errors": exc.error,
            "data" : exc.data
        },
    )


@app.get("/")
def root():
    return {"message": "Server and Database are live!"}
