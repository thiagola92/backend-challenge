from sqlalchemy import Column, String

from src.orm import Base


class Customer(Base):
    __tablename__ = "customers"

    id = Column(String, primary_key=True)
    name = Column(String)
