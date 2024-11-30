from sqlalchemy import create_engine, Column, Integer, String, MetaData, Table, TEXT, Date
from sqlalchemy.ext.declarative import declarative_base

POSTGRES_DB = "postgres"
POSTGRES_USER = "root"
POSTGRES_PASSWORD = "password"
host = "localhost"
port = 8000


def get_connection():
    return create_engine(
        url=f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{host}:{port}/{POSTGRES_DB}")


Base = declarative_base()
db = get_connection()


class GangMembers(Base):
    __tablename__ = 'gang_members'

    id = Column(Integer, primary_key=True)
    nickname = Column(String(100), nullable=False)
    status = Column(String(50))
    contacts = Column(TEXT)
    specialization = Column(String(100))
    level = Column(Integer)
    join_date = Column(Date)



