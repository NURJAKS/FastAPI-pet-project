from pydantic import BaseModel
from typing import Optional, List


# -------------------------------
# STUDENT SCHEMAS
# -------------------------------

class StudentBase(BaseModel):
    name: str
    age: Optional[int] = None


class StudentCreate(StudentBase):
    group_id: int


class StudentOut(StudentBase):
    id: int
    group_id: Optional[int]

    class Config:
        from_attributes = True  # Pydantic v2


class StudentUpdate(BaseModel):
    name: Optional[str] = None
    age: Optional[int] = None
    group_id: Optional[int] = None

    class Config:
        from_attributes = True


# -------------------------------
# GROUP SCHEMAS
# -------------------------------

class GroupBase(BaseModel):
    name: str


class GroupCreate(GroupBase):
    pass


class GroupOut(GroupBase):
    id: int
    students: List[StudentOut] = []

    class Config:
        from_attributes = True
