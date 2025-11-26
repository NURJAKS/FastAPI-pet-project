from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from db.database import Base

class Group(Base):
    __tablename__ = "groups"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)

    # Relationship: one group -> many students
    students = relationship("Student", back_populates="group", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Group id={self.id} name={self.name}>"
