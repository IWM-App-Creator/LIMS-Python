from jose import jwt, JWTError, ExpiredSignatureError
from datetime import datetime, timedelta, UTC
from app.utils.config import ACCESS_TOKEN_EXPIRE_MINUTES, SECRET_KEY, ALGORITHM

class AuthFunctions:
    
    @staticmethod
    def createJWTToken(user_id: int, email: str):
        expire = datetime.now(UTC) + timedelta(minutes = ACCESS_TOKEN_EXPIRE_MINUTES)
        payload = {
            "user_id": str(user_id),
            "email": str(email),
            "exp": expire
        }
        return jwt.encode(payload, SECRET_KEY, algorithm = ALGORITHM)

    @staticmethod
    def verifyJWTToken(token: str):
        try:
            payload = jwt.decode (
                token,
                SECRET_KEY,
                algorithms = ["HS256"]
            )
            return payload
        except Exception:
            return None

authfnct = AuthFunctions()