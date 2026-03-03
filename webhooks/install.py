import logging
from fastapi import APIRouter, Request
from storage import load_config, save_config
from utils.logging_helper import log_dict
from utils.auth_helper import extract_auth

logger = logging.getLogger(__name__)
router = APIRouter()

@router.post("")
async def install(request: Request):
    try:
        data = await request.json()
    except Exception:
        form = await request.form()
        data = dict(form)
    log_dict(logger, data)

    auth = {}
    extract_auth(auth)

    apps = load_config()
    apps[auth["application_token"]] = auth
    save_config(apps)

    logger.info("✅ OAuth сохранён в конфиг")
    return {"Status": "Ok"}