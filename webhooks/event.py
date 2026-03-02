from Bitrix.call import call
from fastapi import APIRouter, Request
import logging

router = APIRouter()

@router.post("")
async def event(request: Request):
    raw = await request.body()
    logging.info(f"RAW EVENT BODY: {raw.decode(errors='ignore')}")

    try:
        data = await request.json()
    except Exception:
        form = await request.form()
        data = dict(form)

    # SDK хочет auth в виде словаря
    # Берём либо из data["auth"], либо из data["data[BOT][ID][AUTH]"]
    auth_keys = [k for k in data.keys() if k.startswith("auth[")]
    auth = {}
    for k in auth_keys:
        auth[k[5:-1]] = data[k]

    if not auth:
        logging.error("❌ Auth не найден")
        return {"status": "error", "msg": "auth not found"}

    event_type = data.get("event")

    if event_type == "ONIMCONNECTORMESSAGEADD":
        message = data.get("data[MESSAGE][text]")
        chat_id = data.get("data[MESSAGE][chat][id]")

        logging.info(f"Новое сообщение: {message} | chat: {chat_id}")

    return {"status": "ok"}