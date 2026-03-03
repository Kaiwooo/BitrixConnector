import logging
from fastapi import APIRouter, Request
from client.call import call
from storage import load_config
from utils.logging_helper import log_dict

logger = logging.getLogger(__name__)
router = APIRouter()

@router.post("")
async def connector_activate(request: Request):
    apps = load_config()
    if not apps:
        return {"Status": "Error", "Message": "No OAuth config found"}

    try:
        params = await request.json()
    except Exception:
        return {"status": "error", "msg": "Invalid JSON body"}

    if not params:
        return {"status": "error", "msg": "Empty body"}

    _, auth = next(iter(apps.items()))
    try:
        result = await call("imconnector.activate", params, auth)
        log_dict(logger, result)
    except Exception as e:
        return {"status": "error", "msg": str(e)}

    return {
        "Bitrix response": result
    }