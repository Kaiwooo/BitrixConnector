import logging
from fastapi import APIRouter, Request, HTTPException
from client.call import call
from storage import load_config
from utils.logging_helper import log_dict

logger = logging.getLogger(__name__)
router = APIRouter()

@router.post("")
async def bitrix_proxy(request: Request):
    apps = load_config()
    if not apps:
        raise HTTPException(status_code=400, detail="No OAuth config found")

    try:
        body = await request.json()
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid JSON")

    method = body.get("method")
    params = body.get("params", {})

    if not method:
        raise HTTPException(status_code=400, detail="Method is required")

    _, auth = next(iter(apps.items()))

    result = await call(method, params, auth)

    log_dict(logger, {
        "method": method,
        "params": params,
        "result": result
    })

    return result