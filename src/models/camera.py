from sqlalchemy import Boolean, Column, ForeignKey, String

from src.orm import Base


class Camera(Base):
    __tablename__ = "cameras"

    id = Column(String, primary_key=True)
    name = Column(String)
    ip = Column(String)
    is_enabled = Column(Boolean)
    customer_id = Column(String, ForeignKey("customers.id"))
