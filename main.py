import logging
from fastapi import FastAPI
from webhooks import install, event, connector_reg, connector_activate, connector_unreg, connector_list, connector_status, openlines

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)

app = FastAPI()
app.include_router(install.router, prefix="/install")
app.include_router(event.router, prefix="/event")
app.include_router(connector_reg.router, prefix="/connreg")
app.include_router(connector_activate.router, prefix="/connactivate")
app.include_router(connector_unreg.router, prefix="/connunreg")
app.include_router(connector_list.router, prefix="/connlist")
app.include_router(connector_status.router, prefix="/connstatus")
app.include_router(openlines.router, prefix="/openlines")