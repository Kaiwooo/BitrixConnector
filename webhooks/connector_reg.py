from fastapi import APIRouter, Request
from Bitrix.call import call
from storage import load_config

router = APIRouter()

@router.post("")
async def register_connector(request: Request):
    apps = load_config()
    if not apps:
        return {"status": "error", "msg": "OAuth not installed"}

    try:
        params = await request.json()
    except Exception:
        return {"status": "error", "msg": "Invalid JSON body"}

    if not params:
        return {"status": "error", "msg": "Empty body"}

    _, auth = next(iter(apps.items()))

    result = await call("imconnector.register", params, auth)

    return {
        "status": "ok",
        "bitrix_result": result
    }