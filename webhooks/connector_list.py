from fastapi import APIRouter
from Bitrix.call import call
from storage import load_config

router = APIRouter()

@router.post("")
async def connector_list():
    apps = load_config()
    if not apps:
        return {"status": "error", "msg": "OAuth not installed"}

    _, auth = next(iter(apps.items()))

    result = await call("imconnector.list", {}, auth)

    return {
        "status": "ok",
        "bitrix_result": result
    }