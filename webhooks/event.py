import logging
from fastapi import APIRouter, Request
from utils.logging_helper import log_dict

logger = logging.getLogger(__name__)
router = APIRouter()

async def handler_onimconnectormessageadd(data: dict):
    message = data.get("data[MESSAGES][0][message][text]")
    chat_id = data.get("data[MESSAGES][0][chat][id]")
    if message and chat_id:
        logger.info(f"Новое сообщение: {message} | chat: {chat_id}")
    return {"Success": True}

@router.post("")
async def event(request: Request):
    try:
        data = await request.json()
    except Exception:
        form = await request.form()
        data = dict(form)

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