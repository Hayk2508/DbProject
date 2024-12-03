import uvicorn
from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy import create_engine
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.orm import sessionmaker, Session
from starlette import status


from models import Base, GangMember

POSTGRES_DB = "postgres"
POSTGRES_USER = "root"
POSTGRES_PASSWORD = "password"
host = "localhost"
port = 8000


def get_connection():
    return create_engine(
        url=f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{host}:{port}/{POSTGRES_DB}")


SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=get_connection())


def get_db() -> Session:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


Base.metadata.create_all(bind=get_connection())

app = FastAPI()


class GangMembers(BaseModel):
    nickname: str
    status: str
    contacts: str
    specialization: str
    level: int
    join_date: str


@app.post("/gang_members/")
def create_gang_member(gang_member: GangMembers, db: Session = Depends(get_db)):
    stmt = insert(GangMember).values(**gang_member.dict())
    try:
        db.execute(stmt)
        db.commit()
        return {"message": "Gang member added successfully"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8002)
