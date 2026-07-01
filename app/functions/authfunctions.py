from jose import jwt, JWTError, ExpiredSignatureError
from datetime import datetime, timedelta
from app.utils.config import ACCESS_TOKEN_EXPIRE_MINUTES, SECRET_KEY, ALGORITHM

def createJWTToken(user_id: int, email: str):
    expire = datetime.utcnow() + timedelta(minutes = ACCESS_TOKEN_EXPIRE_MINUTES)
    payload = {
        "user_id": str(user_id),
        "email": str(email),
        "exp": expire
    }
    return jwt.encode(payload, SECRET_KEY, algorithm = ALGORITHM)

def verifyJWTToken(token: str):
    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=["HS256"]
        )
        return payload
    except Exception:
        return None