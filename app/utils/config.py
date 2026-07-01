from pathlib import Path
import os

SECRET_KEY = "4f7d9b8c2e1a6d5f8b9c7a3d4e6f1a2b5c8d9e0f1a2b3c4d5e6f7a8b9c0d1e2" # JWT algorithm used for signing the token
ALGORITHM = "HS256" # JWT algorithm used for signing the token
ACCESS_TOKEN_EXPIRE_MINUTES = 1. # JWT token expiration time in minutes

TEMPLATES_BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
