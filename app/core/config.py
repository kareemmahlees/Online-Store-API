import datetime
from pydantic import BaseSettings
from dotenv import load_dotenv

load_dotenv()


class Settings(BaseSettings):
    database: str
    user: str
    port: int
    password: str
    expiray: int
    algorithm: str
    secret_key: str


settings = Settings()
