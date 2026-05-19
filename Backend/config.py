import os
from dotenv import load_dotenv
from urllib.parse import quote_plus

load_dotenv()

class Config:

    if os.getenv("RENDER"):
        SQLALCHEMY_DATABASE_URI = "sqlite:///traveloop.db"

    else:
        DB_USER = os.getenv("DB_USER")
        DB_PASSWORD = os.getenv("DB_PASSWORD")
        DB_HOST = os.getenv("DB_HOST")
        DB_NAME = os.getenv("DB_NAME")

        if DB_USER and DB_PASSWORD and DB_HOST and DB_NAME:
            password = quote_plus(DB_PASSWORD)

            SQLALCHEMY_DATABASE_URI = (
                f"mysql+pymysql://{DB_USER}:{password}@{DB_HOST}/{DB_NAME}"
            )
        else:
            SQLALCHEMY_DATABASE_URI = "sqlite:///traveloop.db"

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.getenv("SECRET_KEY", "traveloop-secret")