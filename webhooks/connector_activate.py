from fastapi import APIRouter, Request
from Bitrix.call import call
from storage import load_config

router = APIRouter()

@router.post("")
async def connector_activate(request: Request):
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

    try:
        result = await call("imconnector.activate", params, auth)
    except Exception as e:
        return {"status": "error", "msg": str(e)}

    return {
        "status": "ok",
        "bitrix_result": result
    }