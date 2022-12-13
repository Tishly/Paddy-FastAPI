from urllib.parse import quote_plus
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import psycopg2
from psycopg2.extras import RealDictCursor
import time


SQLALCHEMY_DATABASE_URL = 'postgres://paddy_user:WcBkrp5xE54mUGws2rFKFRLebHd2jRA7@dpg-cebp98da49965ve4odug-a/paddy'

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