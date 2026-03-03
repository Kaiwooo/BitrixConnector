import logging
from fastapi import APIRouter, Request
from client.call import call
from storage import load_config
from utils.logging_helper import log_dict

logger = logging.getLogger(__name__)
router = APIRouter()

@router.post("")
async def connector_status(request: Request):
    apps = load_config()
    if not apps:
        return {"Status": "Error", "Message": "No OAuth config found"}

    try:
        params = await request.json()
    except Exception:
        return {"status": "error", "msg": "Invalid JSON body"}

    _, auth = next(iter(apps.items()))
    result = await call("imconnector.status", params, auth)
    log_dict(logger, result)
    return {
        "Bitrix response": result
    }