from pydantic import BaseSettings

class Settings(BaseSettings):
    # Database Settings
    DATABASE_USER = 'postgres'
    DATABASE_PASS = 'postgres'
    DATABASE_HOST = 'localhost'
    DATABASE_PORT = '5432'
    DATABASE_NAME = 'library'
    DATABASE_URL = f'postgresql://{DATABASE_USER}:{DATABASE_PASS}@{DATABASE_HOST}:{DATABASE_PORT}/{DATABASE_NAME}'

    # App Settings
    APP_NAME = 'Library API'
    APP_TITLE = 'Library API'
    APP_VERSION = '0.1.0'
    APP_DESCRIPTION = 'A simple Library API implementation'


ConfigSettings = Settings()