import os
from dotenv import load_dotenv
from urllib.parse import quote_plus

load_dotenv()

password = quote_plus(os.getenv("DB_PASSWORD"))

class Config:
    SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{os.getenv('DB_USER')}:{password}@{os.getenv('DB_HOST')}/{os.getenv('DB_NAME')}"
    
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    SECRET_KEY = os.getenv("SECRET_KEY")