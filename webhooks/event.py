import logging
from fastapi import APIRouter, Request
from utils.logging_helper import log_dict
from client.call import call

logger = logging.getLogger(__name__)
router = APIRouter()

async def handler_onimconnectormessageadd(data: dict):
    log_dict(logger, {"Inbound Event": data})
    params = {
        "CONNECTOR": data.get("data[CONNECTOR]"),
        "LINE": data.get("data[LINE]"),
        "MESSAGES[0][im][chat_id]": data.get("data[MESSAGES][0][im][chat_id]"),
        "MESSAGES[0][im][message_id]": data.get("data[MESSAGES][0][im][message_id]"),
        #"MESSAGES[0][message][id][0]": data.get("data[MESSAGES][0][im][message_id]"),
        "MESSAGES[0][chat][id]": data.get("data[MESSAGES][0][chat][id]")
    }
    auth = {
        "access_token": data.get("auth[access_token]"),
        "client_endpoint": data.get("auth[client_endpoint]")
    }
    result = await call("imconnector.send.status.delivery", params, auth)
    log_dict(logger, {"Delivery result": result})


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