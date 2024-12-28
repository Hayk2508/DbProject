import uvicorn
from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel
from settings import POSTGRES_USER, POSTGRES_PASSWORD, host, port, POSTGRES_DB
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

from models import Base, GangMember


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


class GangMemberResponse(GangMembers):
    id: int

    class Config:
        orm_mode = True


@app.post("/gang_members/", response_model=GangMemberResponse)
def create_gang_member(gang_member: GangMembers, db: Session = Depends(get_db)):
    new_gang_member = GangMember(**gang_member.dict())

    db.add(new_gang_member)
    db.commit()
    db.refresh(new_gang_member)

    return new_gang_member


@app.get("/gang_members/", response_model=list[GangMemberResponse])
def get_all_gang_members(db: Session = Depends(get_db)):
    gang_members = db.query(GangMember).all()
    return gang_members


@app.get("/gang_members/{member_id}", response_model=GangMemberResponse)
def get_gang_member(member_id: int, db: Session = Depends(get_db)):
    member = db.query(GangMember).filter(GangMember.id == member_id).first()
    if not member:
        raise HTTPException(status_code=404, detail="Gang member not found")
    return member


@app.put("/gang_members/{member_id}", response_model=GangMemberResponse)
def update_gang_member(member_id: int, gang_member: GangMembers, db: Session = Depends(get_db)):
    member = db.query(GangMember).filter(GangMember.id == member_id).first()

    if not member:
        raise HTTPException(status_code=404, detail="Gang member not found")

    for key, value in gang_member.dict().items():
        setattr(member, key, value)

    db.commit()
    db.refresh(member)

    return member


@app.delete("/gang_members/{member_id}")
def delete_gang_member(member_id: int, db: Session = Depends(get_db)):
    member = db.query(GangMember).filter(GangMember.id == member_id).first()
    if not member:
        raise HTTPException(status_code=404, detail="Gang member not found")

    db.delete(member)
    db.commit()

    return {"message": "Gang member deleted successfully"}













if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8002)
