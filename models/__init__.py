from db.database import Base
# импортируем модели чтобы alembic/autogenerate видел metadata
from .group import Group
from .student import Student
