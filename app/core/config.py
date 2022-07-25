from pydantic import BaseSettings
from dotenv import load_dotenv
import os

load_dotenv()


class Settings(BaseSettings):
    database: str
    user: str
    port: int
    password: str


settings = Settings(
    database=os.getenv("database"),
    user=os.getenv("user"),
    port=os.getenv("port"),
    password=os.getenv("password"),
)
#
