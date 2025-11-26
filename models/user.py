# models/user.py
import uuid
from sqlalchemy import Column, String, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from db.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String, unique=True, nullable=False)
    password_hash = Column(String, nullable=True)
    google_id = Column(String, unique=True, nullable=True)
    status = Column(String, default="active")
    created_at = Column(DateTime, server_default=func.now())
    last_login = Column(DateTime)

    role = Column(String, default="user")  # <-- ДОЛЖНО БЫТЬ ТУТ
