from fastapi import APIRouter
from app.controllers.v1 import chatbotcontroller as chatbotapi

router = APIRouter(prefix = "/chatbot")

ROUTES = [
    ("/quesans", chatbotapi.cbQuestionAnswer, ["GET", "POST"])
    ("/saveimg", chatbotapi.cbSaveImage, ["GET", "POST"])
    ("/assistant", chatbotapi.getChatBotAssistant, ["GET"]),
    ("/modules/get", chatbotapi.getCBModules, ["GET"]),
    ("/modules/save", chatbotapi.saveCBModules, ["GET", "POST"])
]

for path, handler, methods in ROUTES:
    router.add_api_route(path, handler, methods=methods)

# chatbotmodule
# cbassistant