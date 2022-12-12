from pydantic import BaseSettings
from dotenv import load_dotenv
from dotenv import dotenv_values
from pathlib import Path
import os

load_dotenv()
env_path = Path('..')/'.env'
load_dotenv(dotenv_path=env_path)

class Settings():
    database_hostname = os.getenv("DATABASE_HOSTNAME")
    database_name = os.getenv("DATABASE_NAME")
    database_password = os.getenv("DATABASE_PASSWORD")
    database_algorithm = os.getenv("DATABASE_ALGORITHM")
    secret_key = os.getenv("SECRET_KEY")
    token_expire_days = os.getenv("TOKEN_EXPIRE_DAYS")
    database_port = os.getenv("DATABASE_PORT")
    database_username = os.getenv("DATABASE_USERNAME")

    class Config:
        env_file = '../.env'
        # env_file_encoding='utf-8'

settings = Settings()
