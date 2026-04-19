from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
import datetime
from database import Base

class Incident(Base):
    __tablename__ = "incidents"

    id = Column(Integer, primary_key=True, index=True)
    text = Column(String, index=True)
    type = Column(String) # FIRE, MEDICAL, SECURITY
    severity = Column(String) # HIGH, MEDIUM, LOW
    location = Column(String)
    status = Column(String, default="ACTIVE")
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    resolved_at = Column(DateTime, nullable=True)

    messages = relationship("ChatMessage", back_populates="incident")

class ChatMessage(Base):
    __tablename__ = "chat_messages"

    id = Column(Integer, primary_key=True, index=True)
    incident_id = Column(Integer, ForeignKey("incidents.id"))
    sender = Column(String)
    message = Column(Text)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)

    incident = relationship("Incident", back_populates="messages")
