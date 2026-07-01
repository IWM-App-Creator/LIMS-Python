from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.initialize.initialize import initialize
from app.routehelper.router import routerGroup

from app.requesthelper.errorhandler import error_handler
from app.requesthelper.requestcontext import request_context
from app.requesthelper.auth import auth_middleware

app = FastAPI()

@app.get("/")
def root():
    return {"status": "True"}

@app.on_event("startup")
async def startup_event():
    initialize()

# Include Router
app.include_router(routerGroup())

app.middleware("http")(error_handler)
app.middleware("http")(request_context)
app.middleware("http")(auth_middleware)

# Middleware for CORS
app.add_middleware (
    CORSMiddleware,
    allow_origins =[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://127.0.0.1:8000"
    ],
    allow_credentials = True,
    allow_methods = ["*"],
    allow_headers = ["*"],
)