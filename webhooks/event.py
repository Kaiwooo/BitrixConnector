import logging
from fastapi import APIRouter, Request
from utils.logging_helper import log_dict
from client.call import call

logger = logging.getLogger(__name__)
router = APIRouter()

async def handler_onimconnectormessageadd(data: dict):
    log_dict(logger, {"Inbound Event": data})
    connector_id = data.get("data[CONNECTOR]")
    line_id = data.get("data[LINE]")
    message = data.get("data[MESSAGES][0][im][chat]")
    chat_id = data.get("data[MESSAGES][0][im][id]")
    message_id = data.get("data[MESSAGES][0][im][message_id]")
    params = {
        "CONNECTOR": connector_id,
        "LINE": line_id,
        "MESSAGES[0][CHAT_ID]": chat_id,
        "MESSAGES[0][MESSAGE_ID]": message_id
    }
    auth = data.get("AUTH[access_token]")
    app_token = data.get("AUTH[app_token]")
    result = await call("imconnector.send.status.delivery", params, auth, app_token)
    return result


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