from jose import jwt
from jose.exceptions import ExpiredSignatureError, JWTError
from datetime import datetime, timedelta, UTC
from app.utils.config import ACCESS_TOKEN_EXPIRE_MINUTES, SECRET_KEY, ALGORITHM

class AuthFunctions:
    
    @staticmethod
    def createJWTToken(user_id: int, role_id: int, email: str):
        expire = datetime.now(UTC) + timedelta(minutes = ACCESS_TOKEN_EXPIRE_MINUTES)
        payload = {
            "user_id": str(user_id),
            "role_id": str(role_id),
            "email": str(email),
            "exp": expire
        }
        return jwt.encode(payload, SECRET_KEY, algorithm = ALGORITHM)

    @staticmethod
    def createFPJWTToken(user_id: int, email: str):
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
            payload = jwt.decode(
                token,
                SECRET_KEY,
                algorithms=[ALGORITHM]
            )
            return {
                "status": True,
                "payload": payload
            }

        except ExpiredSignatureError:
            return {
                "status": False,
                "message": "Token has expired."
            }

        except JWTError:
            return {
                "status": False,
                "message": "Invalid token."
            }

    #Validate existing token and return a fresh JWT with a new expiry.
    @staticmethod
    def refreshJWTToken(old_token: str) -> str | None:
        payload = authfnct.verifyJWTToken(old_token)
        if payload is None:
            return None
        return authfnct.createJWTToken(
            user_id=int(payload["user_id"]),
            role_id=int(payload["role_id"]),
            email=payload["email"],
        )
authfnct = AuthFunctions()