from sqlalchemy import Column, Integer, String, Date, ForeignKey, DECIMAL, Text, Index
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()


class GangMember(Base):
    __tablename__ = 'gang_members'

    id = Column(Integer, primary_key=True, index=True)
    nickname = Column(String(100), nullable=False)
    status = Column(String(50))
    contacts = Column(Text)
    specialization = Column(String(100))
    level = Column(Integer)
    join_date = Column(Date)

    weight = Column(DECIMAL, nullable=True)
    height = Column(DECIMAL, nullable=True)

    __table_args__ = (
        Index('ix_nickname', 'nickname'),
    )

    robberies = relationship("Robbery", back_populates="gang_member")


class Bank(Base):
    __tablename__ = 'banks'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(150), nullable=False)
    address = Column(Text)
    attractiveness = Column(DECIMAL(5, 2))
    daily_income = Column(DECIMAL(10, 2))
    security_level = Column(Integer)

    robberies = relationship("Robbery", back_populates="bank")


class Robbery(Base):
    __tablename__ = 'robberies'

    id = Column(Integer, primary_key=True, index=True)
    robbery_date = Column(Date)
    action_rating = Column(Integer)
    bandit_outcome = Column(Text)
    share = Column(DECIMAL(5, 2))

    gang_member_id = Column(Integer, ForeignKey('gang_members.id'), nullable=False)
    bank_id = Column(Integer, ForeignKey('banks.id'), nullable=False)

    gang_member = relationship("GangMember", back_populates="robberies")
    bank = relationship("Bank", back_populates="robberies")
