from urllib.parse import quote_plus
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from .config import settings

SQLALCHEMY_DATABASE_URL = 'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}' # % quote_plus({settings.database_password})

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# while True:
   # try:
    #    conn = psycopg2.connect(host="localhost", database="Paddy", user="postgres", password="$here@!post",
    #                             cursor_factory=RealDictCursor)
    #     cursor = conn.cursor()
    #     print("Database connected successfully")
    #     break
    # except Exception as error:
    #     time.sleep(20)
    #     print("Connection to database failed")
    #     print("Error: ", error)