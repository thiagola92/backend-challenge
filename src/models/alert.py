from sqlalchemy import TIMESTAMP, Column, ForeignKey, String

from src.orm import Base


class Alert(Base):
    __tablename__ = "alert_logs"

    id = Column(String, primary_key=True)
    occurred_at = Column(TIMESTAMP)
    camera_id = Column(String, ForeignKey("cameras.id"))
