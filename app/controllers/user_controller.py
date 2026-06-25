from fastapi import HTTPException

async def login():
    return {
        "success": True,
        "message": "Login successful"
    }

async def check_token():
    return {
        "valid": True
    }