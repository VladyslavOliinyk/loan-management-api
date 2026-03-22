from sqlalchemy import Column, Date, ForeignKey, Integer, Numeric, String
from sqlalchemy.orm import relationship

from app.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    login = Column(String(255), nullable=False)
    registration_date = Column(Date, nullable=False)

    credits = relationship("Credit", back_populates="user")


class Credit(Base):
    __tablename__ = "credits"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    issuance_date = Column(Date, nullable=False)
    return_date = Column(Date, nullable=False)
    actual_return_date = Column(Date, nullable=True)
    body = Column(Numeric(12, 2), nullable=False)
    percent = Column(Numeric(12, 2), nullable=False)

    user = relationship("User", back_populates="credits")
    payments = relationship("Payment", back_populates="credit")


class Dictionary(Base):
    __tablename__ = "dictionary"

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)


class Plan(Base):
    __tablename__ = "plans"

    id = Column(Integer, primary_key=True)
    period = Column(Date, nullable=False)
    sum = Column(Numeric(12, 2), nullable=False)
    category_id = Column(Integer, ForeignKey("dictionary.id"), nullable=False)

    category = relationship("Dictionary")


class Payment(Base):
    __tablename__ = "payments"

    id = Column(Integer, primary_key=True)
    sum = Column(Numeric(12, 2), nullable=False)
    payment_date = Column(Date, nullable=False)
    credit_id = Column(Integer, ForeignKey("credits.id"), nullable=False)
    type_id = Column(Integer, ForeignKey("dictionary.id"), nullable=False)

    credit = relationship("Credit", back_populates="payments")
    type = relationship("Dictionary")
