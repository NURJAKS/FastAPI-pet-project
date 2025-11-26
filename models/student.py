from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from db.database import Base

class Student(Base):
    __tablename__ = "students"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    age = Column(Integer)
    group_id = Column(Integer, ForeignKey("groups.id", ondelete="CASCADE"))

    # backlink to group
    group = relationship("Group", back_populates="students")

    def __repr__(self):
        return f"<Student id={self.id} name={self.name} age={self.age} group_id={self.group_id}>"


