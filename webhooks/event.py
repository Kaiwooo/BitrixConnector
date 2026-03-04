import logging
#from client.call import call
from fastapi import APIRouter, Request
from utils.auth_helper import extract_auth
from utils.logging_helper import log_dict

logger = logging.getLogger(__name__)
router = APIRouter()

async def handler_onimconnectormessageadd(data: dict):
    message = data.get("data[MESSAGE][text]")
    chat_id = data.get("data[MESSAGE][chat][id]")
    if message and chat_id:
        logger.info(f"Новое сообщение: {message} | chat: {chat_id}")

@router.post("")
async def event(request: Request):
    try:
        data = await request.json()
    except Exception:
        form = await request.form()
        data = dict(form)

    log_dict(logger, {"Inbound Event": data})

    if data.get("PLACEMENT"):
        logger.info(f"Placement call: {data.get('PLACEMENT')}")
        return {"status": "success"}

    #auth = extract_auth(data)
    event_type = data.get("event")

    handlers = {
        "ONIMCONNECTORMESSAGEADD": handler_onimconnectormessageadd
    }
    handler = handlers.get(event_type)

    if handler:
        await handler(data)
    else:
        log_dict(logger, {"Inbound Event": data})

    return {"Status": "ok"}