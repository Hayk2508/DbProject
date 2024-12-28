from datetime import date

import uvicorn
from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.exc import IntegrityError

from settings import POSTGRES_USER, POSTGRES_PASSWORD, host, port, POSTGRES_DB
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

from models import Base, GangMember, Bank, Robbery


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


class GangMemberBase(BaseModel):
    nickname: str
    status: str
    contacts: str
    specialization: str
    level: int
    join_date: date


class GangMemberResponse(GangMemberBase):
    id: int

    class Config:
        orm_mode = True


class BankBase(BaseModel):
    name: str
    address: str
    attractiveness: float
    daily_income: float
    security_level: int


class BankResponse(BankBase):
    id: int

    class Config:
        orm_mode = True


class RobberyBase(BaseModel):
    robbery_date: date
    action_rating: int
    bandit_outcome: str
    share: float
    gang_member_id: int
    bank_id: int


class RobberyResponse(RobberyBase):
    id: int

    class Config:
        orm_mode = True


@app.post("/gang_members/", response_model=GangMemberResponse)
def create_gang_member(gang_member: GangMemberBase, db: Session = Depends(get_db)):
    new_gang_member = GangMember(**gang_member.dict())

    db.add(new_gang_member)
    db.commit()
    db.refresh(new_gang_member)

    return new_gang_member


@app.get("/gang_members/", response_model=list[GangMemberResponse])
def get_all_gang_members(db: Session = Depends(get_db)):
    return db.query(GangMember).all()


@app.get("/gang_members/{member_id}", response_model=GangMemberResponse)
def get_gang_member(member_id: int, db: Session = Depends(get_db)):
    member = db.query(GangMember).filter(GangMember.id == member_id).first()
    if not member:
        raise HTTPException(status_code=404, detail="Gang member not found")
    return member


@app.put("/gang_members/{member_id}", response_model=GangMemberResponse)
def update_gang_member(member_id: int, gang_member: GangMemberBase, db: Session = Depends(get_db)):
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


@app.post("/banks/", response_model=BankResponse)
def create_bank(bank: BankBase, db: Session = Depends(get_db)):
    new_bank = Bank(**bank.dict())

    db.add(new_bank)
    db.commit()
    db.refresh(new_bank)

    return new_bank


@app.get("/banks/", response_model=list[BankResponse])
def get_all_banks(db: Session = Depends(get_db)):
    return db.query(Bank).all()


@app.get("/banks/{bank_id}", response_model=BankResponse)
def get_bank(bank_id: int, db: Session = Depends(get_db)):
    bank = db.query(Bank).filter(Bank.id == bank_id).first()
    if not bank:
        raise HTTPException(status_code=404, detail="Bank not found")
    return bank


@app.put("/banks/{bank_id}", response_model=BankResponse)
def update_bank(bank_id: int, bank: BankBase, db: Session = Depends(get_db)):
    existing_bank = db.query(Bank).filter(Bank.id == bank_id).first()

    if not existing_bank:
        raise HTTPException(status_code=404, detail="Bank not found")

    for key, value in bank.dict().items():
        setattr(existing_bank, key, value)

    db.commit()
    db.refresh(existing_bank)

    return existing_bank


@app.delete("/banks/{bank_id}")
def delete_bank(bank_id: int, db: Session = Depends(get_db)):
    bank = db.query(Bank).filter(Bank.id == bank_id).first()

    if not bank:
        raise HTTPException(status_code=404, detail="Bank not found")

    db.delete(bank)
    db.commit()

    return {"message": "Bank deleted successfully"}



@app.post("/robberies/", response_model=RobberyResponse)
def create_robbery(robbery: RobberyBase, db: Session = Depends(get_db)):
    new_robbery = Robbery(**robbery.dict())
    try:
        db.add(new_robbery)
        db.commit()
        db.refresh(new_robbery)
        return {"message": "Robbery created successfully", "robbery": new_robbery}
    except IntegrityError as e:
        db.rollback()
        raise HTTPException(status_code=400, detail="Invalid bank_id or gang_member_id.")

@app.get("/robberies/", response_model=list[RobberyResponse])
def get_all_robberies(db: Session = Depends(get_db)):
    return db.query(Robbery).all()

@app.get("/robberies/{robbery_id}", response_model=RobberyResponse)
def get_robbery(robbery_id: int, db: Session = Depends(get_db)):
    robbery = db.query(Robbery).filter(Robbery.id == robbery_id).first()

    if not robbery:
        raise HTTPException(status_code=404, detail="Robbery not found")

    return robbery

@app.put("/robberies/{robbery_id}", response_model=RobberyResponse)
def update_robbery(robbery_id: int, robbery: RobberyBase, db: Session = Depends(get_db)):
    existing_robbery = db.query(Robbery).filter(Robbery.id == robbery_id).first()

    if not existing_robbery:
        raise HTTPException(status_code=404, detail="Robbery not found")

    for key, value in robbery.dict().items():
        setattr(existing_robbery, key, value)

    db.commit()
    db.refresh(existing_robbery)

    return existing_robbery

@app.delete("/robberies/{robbery_id}")
def delete_robbery(robbery_id: int, db: Session = Depends(get_db)):
    robbery = db.query(Robbery).filter(Robbery.id == robbery_id).first()
    if not robbery:
        raise HTTPException(status_code=404, detail="Robbery not found")
    db.delete(robbery)
    db.commit()
    return {"message": "Robbery deleted successfully"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8002)
