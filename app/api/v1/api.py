from fastapi import APIRouter
from app.controllers.user_controller import login, check_token

router = APIRouter(prefix="/users", tags=["Users"])

router.get("/login")(login)
router.get("/check-token")(check_token)