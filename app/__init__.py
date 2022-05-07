from fastapi import FastAPI

from app.instance.config import ConfigSettings
from app.services.database import create_db_and_tables


app = FastAPI(
    name=ConfigSettings.APP_NAME,
    title=ConfigSettings.APP_TITLE,
    version=ConfigSettings.APP_VERSION,
    description=ConfigSettings.APP_DESCRIPTION,
)


@app.on_event("startup")
def on_startup():
    create_db_and_tables()
