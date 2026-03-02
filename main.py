from fastapi import FastAPI
from webhooks import install, event
import logging

logging.basicConfig(level=logging.INFO)

app = FastAPI()

app.include_router(install.router, prefix="/install")
app.include_router(event.router, prefix="/event")