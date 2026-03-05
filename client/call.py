import httpx
import logging
from client.refresh_token import refresh_token
from storage import load_config, save_config

logger = logging.getLogger(__name__)

async def call(method: str, params: dict, auth: dict, app_token: str = None):

    url = f"{auth['client_endpoint']}{method}"

    params = params.copy()
    params["auth"] = auth["access_token"]

    logger.debug(f"REST CALL: {url}")
    logger.debug(f"params={params}")

    async with httpx.AsyncClient() as client:

        resp = await client.post(url, data=params)

        try:
            result = resp.json()
        except Exception:
            logger.error(resp.text)
            raise

        if result.get("error") in ("expired_token", "invalid_token"):

            logger.debug("Token expired, refreshing...")

            new_auth = await refresh_token(auth)

            if new_auth and app_token:

                cfg = load_config()
                cfg[app_token] = new_auth
                save_config(cfg)

                auth = new_auth
                params["auth"] = auth["access_token"]

                resp = await client.post(url, data=params)
                result = resp.json()

            else:
                logger.error("Token refresh failed")

        return result