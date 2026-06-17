# from fastapi import FastAPI
# from app.routes.users import router as user_router

# app = FastAPI()

# app.include_router(user_router)

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes.users import router as user_router
from app.firebase_service import init_firebase


app = FastAPI()

@app.on_event("startup")
async def startup_event():
    init_firebase()
    print("Firebase initialized")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user_router)