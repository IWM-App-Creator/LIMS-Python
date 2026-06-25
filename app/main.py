from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1.users import router as user_router
from app.api.v1.pdf import router as pdf_router
from app.api.v1.barcode import router as barcode_router

from app.services.firebase_service import init_firebase

app = FastAPI()

@app.get("/")
def root():
    return {"status": "True"}

@app.on_event("startup")
async def startup_event():
    init_firebase()
    print("Firebase initialized")


app.include_router(user_router)
app.include_router(pdf_router)
app.include_router(barcode_router)


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