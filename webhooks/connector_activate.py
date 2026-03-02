from fastapi import APIRouter, Request
from Bitrix.call import call
from storage import load_config

router = APIRouter()

@router.post("")
async def register_connector(request: Request):
    apps = load_config()