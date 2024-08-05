from sqlalchemy import Column, Date, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.mysql import JSON
from sqlalchemy import DateTime
import datetime
from api.db import Base

class Mindmap(Base):
    __tablename__ = "mindmaps"
    id = Column(Integer, primary_key=True)
    title = Column(String(64), nullable=False)
    registration_date = Column(DateTime, default=datetime.datetime.utcnow)
    nodes_json = Column(JSON, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    user = relationship("User", back_populates="mindmap")
