from fastapi import APIRouter, Request
from Bitrix.call import call
from storage import load_config

router = APIRouter()

@router.post("")
async def connector_list(request: Request):
    apps = load_config()
    if not apps:
        return {"status": "error", "msg": "OAuth not installed"}

    auth = next(iter(apps.items()))

    result = await call("imconnector.list", auth)

    return {
        "status": "ok",
        "bitrix_result": result
    }