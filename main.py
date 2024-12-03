from sqlalchemy import create_engine
from models import Base

POSTGRES_DB = "postgres"
POSTGRES_USER = "root"
POSTGRES_PASSWORD = "password"
host = "localhost"
port = 8000


def get_connection():
    return create_engine(
        url=f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{host}:{port}/{POSTGRES_DB}")


db = get_connection()

Base.metadata.create_all(bind=get_connection())





