from fastapi import FastAPI
from webhooks import install, event, connector_reg, connector_activate, connector_unreg
import logging

logging.basicConfig(level=logging.INFO)

app = FastAPI()

app.include_router(install.router, prefix="/install")
app.include_router(event.router, prefix="/event")
app.include_router(connector_reg.router, prefix="/connector_register")
app.include_router(connector_activate.router, prefix="/connector_activate")
app.include_router(connector_unreg.router, prefix="/connector_unregister")