from jose import jwt, JWTError, ExpiredSignatureError
from datetime import datetime, timedelta
from app.utils.config import ACCESS_TOKEN_EXPIRE_MINUTES, SECRET_KEY, ALGORITHM

def create_token(user_id: int, email: str):
    expire = datetime.utcnow() + timedelta(minutes = ACCESS_TOKEN_EXPIRE_MINUTES)
    payload = {
        "user_id": str(user_id),
        "email": str(email),
        "exp": expire
    }
    return jwt.encode(payload, SECRET_KEY, algorithm = ALGORITHM)

# def verify_token(token: str):
#     try:
#         payload = jwt.decode (
#             token,
#             SECRET_KEY,
#             algorithms=[ALGORITHM]
#         )
#         return {
#             "valid": True,
#             "user_id": payload.get("user_id"),
#             "email": payload.get("email")
#         }
#     except ExpiredSignatureError:
#         return {
#             "valid": False,
#             "message": "Token expired"
#         }
#     except JWTError:
#         return {
#             "valid": False,
#             "message": "Invalid token"
#         }

def verify_token(token: str):
    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=["HS256"]
        )
        return payload
    except Exception:
        return None