from fastapi import FastAPI
from dotenv import load_dotenv
from pathlib import Path

from fastapi.middleware.cors import CORSMiddleware
from app.initialize import initialize
from app.routehelper.router import routerGroup

from app.requesthelper.errorhandler import error_handler
from app.requesthelper.requestcontext import request_context
from app.requesthelper.authhandler import auth_handler

from app.functions.generalfunctions import gnrlfnct

load_dotenv(Path(__file__).parent.parent / ".env")

app = FastAPI()

@app.get("/")
def root():
    return {"status": "True"}

@app.on_event("startup")
async def startup_event():
    initialize()

# Set Env Variables To Global Properties.
gnrlfnct.setEnvVariables()

# Include Router.
app.include_router(routerGroup())

# Middleware for Request Context, Error Handler, Authentication and Workspace
app.middleware("http")(error_handler)
app.middleware("http")(request_context)
app.middleware("http")(auth_handler)

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