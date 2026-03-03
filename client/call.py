import httpx
import logging
from client.refresh_token import refresh_token
from storage import load_config, save_config

logger = logging.getLogger(__name__)

async def call(method: str, params: dict, auth: dict, app_token: str = None):
    """
    Bitrix REST API с авто-обновлением токена.
    :param method: метод REST API, например "imbot.bot.list"
    :param params: параметры запроса
    :param auth: словарь с auth данными
    :param app_token: ключ приложения в конфиге (для сохранения обновленного токена)
    """
    url = f"{auth['client_endpoint']}{method}"
    params["auth"] = auth["access_token"]

    logger.debug(f"REST CALL: {url} | params={params}")
    logger.debug(f"params={params}")

    async with httpx.AsyncClient() as client:
        resp = await client.post(url, data=params)
        result = resp.json()

    # Проверка на устаревший или недействительный токен
    if "error" in result and result["error"] in ("expired_token", "invalid_token"):
        logger.debug("Token expired, refreshing...")
        new_auth = await refresh_token(auth)
        if new_auth and app_token:
            # Сохраняем обновленный токен в конфиг
            cfg = load_config()
            cfg[app_token] = new_auth
            save_config(cfg)
            auth = new_auth
            params["auth"] = auth["access_token"]
            # Повторяем запрос с новым токеном
            async with httpx.AsyncClient() as client:
                resp = await client.post(url, data=params)
                result = resp.json()
        else:
            logger.debug(f"Token refresh failed or no app_token provided")
    return result