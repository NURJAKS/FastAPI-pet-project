# api/app.py  (фрагменты с Redis)
from fastapi import FastAPI, Depends, HTTPException
from starlette.middleware.sessions import SessionMiddleware
from sqlalchemy.orm import Session
from db.database import engine, Base, get_db
from models.group import Group
from models.student import Student
from api.schemas import GroupCreate, GroupOut, StudentCreate, StudentOut, StudentUpdate
from db.redis_client import get_redis_client
import json
from typing import List
from api.auth_routes import router as auth_router
from api.protected_routes import router as protected_router


app = FastAPI()

Base.metadata.create_all(bind=engine)

app.add_middleware(
    SessionMiddleware,
    secret_key="mysuperstrongsecretkey1234567890",
)

app.include_router(auth_router)
app.include_router(protected_router)


# ключи кэша — простая конвенция
ALL_STUDENTS_KEY = "students:all"
STUDENT_KEY_FMT = "student:{id}"

CACHE_TTL = 60  # seconds — время жизни кэша, настрой как нужно

# GET /students — с кэшем
@app.get("/students", response_model=List[StudentOut])
async def read_students(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    r = get_redis_client()
    # попытка получить из кэша (храним как JSON)
    cache = await r.get(ALL_STUDENTS_KEY)
    if cache:
        # парсим JSON и возвращаем (Pydantic orm_mode будет принимать dict)
        students_list = json.loads(cache)
        # можно применить skip/limit уже к cached list, но тут кешируем весь список
        return students_list[skip: skip + limit]

    # кеша нет — берем из БД и кладём в Redis
    students = db.query(Student).offset(skip).limit(limit).all()
    # сериализуем в простой список dict
    data = [ {"id": s.id, "name": s.name, "age": s.age, "group_id": s.group_id} for s in students ]
    # сохраняем полный список (без slice) для простоты
    await r.set(ALL_STUDENTS_KEY, json.dumps(data), ex=CACHE_TTL)
    return data

# GET /students/{id} — с кэшем для конкретного студента
@app.get("/students/{student_id}", response_model=StudentOut)
async def read_student(student_id: int, db: Session = Depends(get_db)):
    r = get_redis_client()
    key = STUDENT_KEY_FMT.format(id=student_id)
    cache = await r.get(key)
    if cache:
        return json.loads(cache)

    student = db.get(Student, student_id)
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    data = {"id": student.id, "name": student.name, "age": student.age, "group_id": student.group_id}
    await r.set(key, json.dumps(data), ex=CACHE_TTL)
    return data

# POST /students — создаём и инвалидируем кэш
@app.post("/students", response_model=StudentOut, status_code=201)
async def create_student(payload: StudentCreate, db: Session = Depends(get_db)):
    # проверка группы
    if not db.get(Group, payload.group_id):
        raise HTTPException(status_code=400, detail="Group not found")
    s = Student(name=payload.name, age=payload.age, group_id=payload.group_id)
    db.add(s)
    db.commit()
    db.refresh(s)

    # инвалидация кэша: удаляем общий список и возможный ключ конкретного студента
    r = get_redis_client()
    await r.delete(ALL_STUDENTS_KEY)
    await r.delete(STUDENT_KEY_FMT.format(id=s.id))
    return {"id": s.id, "name": s.name, "age": s.age, "group_id": s.group_id}

# PUT /students/{id} — обновляем и очищаем кэш
@app.put("/students/{student_id}", response_model=StudentOut)
async def update_student(student_id: int, payload: StudentUpdate, db: Session = Depends(get_db)):
    student = db.get(Student, student_id)
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    for key, value in payload.dict(exclude_unset=True).items():
        setattr(student, key, value)
    db.commit()
    db.refresh(student)

    r = get_redis_client()
    await r.delete(ALL_STUDENTS_KEY)
    await r.set(STUDENT_KEY_FMT.format(id=student_id),
                json.dumps({"id": student.id, "name": student.name, "age": student.age, "group_id": student.group_id}),
                ex=CACHE_TTL)
    return {"id": student.id, "name": student.name, "age": student.age, "group_id": student.group_id}

# DELETE — удаляем и инвалидируем
@app.delete("/students/{student_id}", status_code=204)
async def delete_student(student_id: int, db: Session = Depends(get_db)):
    student = db.get(Student, student_id)
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    db.delete(student)
    db.commit()

    r = get_redis_client()
    await r.delete(ALL_STUDENTS_KEY)
    await r.delete(STUDENT_KEY_FMT.format(id=student_id))
    return
