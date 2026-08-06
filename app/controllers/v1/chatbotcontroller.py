import json
import os
import requests
from fastapi import APIRouter
# from fastapi.responses import JSONResponse

from app.utils.common import DB, Request, RequestData, JSONResponse, raiseAPIError, raiseInvalidError, nowWithTimeZone, userps, globalps
from app.dbfunctions.logfunctions import saveErrorLogtoDB
# from app.dbfunctions.chatbotfunctions import getViewDataByID, insertUpdateView
from app.helper.chatbothelper import cbhlp
from app.properties.chatbotproperties import cbps

# https://testws1.miidata.dev:5173/api/v1/chatbot/quesans
def cbQuestionAnswer(request: Request):
    try:
        params = RequestData.params(request)
        cbhlp.setCBQuesAnsParam(cbps, params) # Get Input Param Data
        response_text = "Python API is not available at this time."
        strchat_history = ""
        strcb_buttons = []
        strcode = ""
        ai_api_url = globalps.AI_API_URL #os.getenv("AI_API_URL", "https://xytovet.com.au/python_code2").rstrip("/")
        ai_payload = {
            "query": cbhlp.query.get(),
            # "user_id": cbhlp.get("user_id", "1"),
            "workspace_id": cbhlp.workspace_id.get(),
            "type": cbhlp.type.get(),
            "subtype": cbhlp.subtype.get(),
            "view_id": cbhlp.view_id.get(),
            "table_id": cbhlp.table_id.get(),
            "link": cbhlp.link.get(),
            "workspace_url": cbhlp.workspace_url.get(),
            "schema_name": cbhlp.schema_name.get(),
            "workspace_schema": cbhlp.workspace_schema.get(),
            "table_url": cbhlp.table_url.get(),
            "schema_output": cbhlp.schema_output.get(),
            "db_query": cbhlp.db_query.get(),
            "chat_history": cbhlp.chat_history.get(),
            "sys_dashboard_ai_id": cbhlp.sys_dashboard_ai_id.get(),
            "session_id": cbhlp.session_id.get(),
            "integration_id": cbhlp.integration_id.get(),
            "endpoint_id": cbhlp.endpoint_id.get(),
        }
         # Call CURL
        api_response = requests.post(ai_api_url, json=ai_payload, timeout=60)

        # import httpx
        # async with httpx.AsyncClient(timeout=60) as client:
        #     api_response = await client.post(ai_api_url, json=ai_payload)
        #     json_data = api_response.json()

        if api_response.status_code == 200:
            json_data = api_response.json()
            response_text = json_data.get("response", response_text)
            strcb_buttons = json_data.get("cb_buttons", [])
            strcode = json_data.get("code", "")
            strchat_history = json_data.get("chat_history", "")
        return JSONResponse (
            status_code = 500,
            content = {
                "status": True,
                "message": "Chatbot QA",
                "strchat_history": strchat_history,
                "strcb_buttons": strcb_buttons,
                "code": strcode,
                "response": response_text,
            }
        )
    except Exception as e:
        # saveErrorLogtoDB ("View", viewps.view_id.get(), "getViewData", str(e)) # Log Error To DB
        raiseAPIError(str(e), 500)

# https://testws1.miidata.dev:5173/api/v1/chatbot/saveimg
def cbSaveImage (request: Request):
    try:
        params = RequestData.params(request)
    except Exception as e:
        saveErrorLogtoDB ("View", "", "cbSaveImage", str(e)) # Log Error To DB
        raiseAPIError(str(e), 500)

# https://testws1.miidata.dev:5173/api/v1/chatbot/assistant
def getChatBotAssistant(request: Request):
    try:
        params = RequestData.params(request)
    except Exception as e:
        # saveErrorLogtoDB ("View", viewps.view_id.get(), "getViewData", str(e)) # Log Error To DB
        raiseAPIError(str(e), 500)
    # try:
    #     params = RequestData.params(request)
    #     filterps.view_id.set(params.get("view_id", 0))
    #     filter_list = getSaveFilters(filterps)
    #     return JSONResponse(
    #         status_code = 200,
    #         content = {
    #             "status": True,
    #             "message": "Filter Data",
    #             "filter_list": filter_list
    #         }
    #     )
    # except Exception as e:
    #     saveErrorLogtoDB("Filter", filterps.view_id.get(), "getFilters", str(e))
    #     raiseAPIError(str(e), 500)

# https://testws1.miidata.dev:5173/api/v1/chatbot/modules/get
def getCBModules(request: Request):
    try:
        params = RequestData.params(request)
    except Exception as e:
        # saveErrorLogtoDB ("View", viewps.view_id.get(), "getViewData", str(e)) # Log Error To DB
        raiseAPIError(str(e), 500)

# https://testws1.miidata.dev:5173/api/v1/chatbot/modules/save
def saveCBModules(request: Request):
    try:
        params = RequestData.params(request)
    except Exception as e:
        # saveErrorLogtoDB ("View", viewps.view_id.get(), "getViewData", str(e)) # Log Error To DB
        raiseAPIError(str(e), 500)
