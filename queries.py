from db.database import SessionLocal
from models.group import Group
from models.student import Student
from sqlalchemy import select

# --------------------------
#  SQLAlchemy Queries (JOIN, FILTER, UPDATE, DELETE)
# --------------------------

session = SessionLocal()

print("== Groups and their students via relationship ==")
groups = session.query(Group).all()
for g in groups:
    print(g, "students:", [s.name for s in g.students])


print("\n== JOIN students + groups ==")
rows = session.query(Student, Group).join(Group, Student.group).all()
for student, group in rows:
    print(student.name, "->", group.name)


print("\n== select(Student.name, Group.name) using select() ==")
stmt = select(Student.name, Group.name).join(Group)
res = session.execute(stmt).all()
for name, group_name in res:
    print(name, "->", group_name)


print("\n== students age > 20 with group name ==")
stmt = select(Student).join(Group).where(Student.age > 20)
for row in session.execute(stmt).scalars().all():
    print(row.name, row.age, "group_id:", row.group_id)


# UPDATE: переименуем группу
g = session.query(Group).filter_by(name="CS-01").first()
if g:
    print("Before:", g)
    g.name = "CS-001"
    session.commit()
    print("After:", session.query(Group).get(g.id))


# DELETE: удаляем Samat
s = session.query(Student).filter_by(name="Samat").first()
if s:
    session.delete(s)
    session.commit()
    print("Deleted Samat")

session.close()



# --------------------------
#  Redis Cache Demo
# --------------------------

import redis
import json

print("\n=== Redis demo ===")

# подключение к local Redis
r = redis.Redis(
    host="localhost",
    port=6379,
    db=0,
    decode_responses=True
)

# DEBUG: показать статистику Redis
try:
    print("DEBUG: redis info loaded!")
    info = r.info()
    print("DEBUG: connected to Redis, keys:", info.get("db0", {}))
except Exception as e:
    print("ERROR: Cannot connect to Redis:", e)


# ПРОБУЕМ ПОЛУЧИТЬ КЭШ
cache = r.get("students:all")

if cache:
    print("From cache:", json.loads(cache))

else:
    print("DEBUG: cache MISS → querying DB")

    session = SessionLocal()
    students = session.query(Student).all()

    print("DEBUG: queried students =", students)

    data = [
        {
            "id": s.id,
            "name": s.name,
            "age": s.age,
            "group_id": s.group_id
        }
        for s in students
    ]

    # кладем в Redis
    r.set("students:all", json.dumps(data), ex=60)
    print("DEBUG: key 'students:all' written!")

    print("From db:", data)

    session.close()
