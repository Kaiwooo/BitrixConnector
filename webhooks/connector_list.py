import logging
from fastapi import APIRouter
from client.call import call
from storage import load_config
from utils.logging_helper import log_dict

logger = logging.getLogger(__name__)
router = APIRouter()

@router.post("")
async def connector_list():
    apps = load_config()
    if not apps:
        return {"Status": "Error", "Message": "No OAuth config found"}

    _, auth = next(iter(apps.items()))
    result = await call("imconnector.list", {}, auth)
    log_dict(logger, result)
    return {
        "Bitrix Response": result
    }