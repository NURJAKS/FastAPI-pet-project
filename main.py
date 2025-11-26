from db.database import engine, Base, SessionLocal
from models.group import Group
from models.student import Student

if __name__ == "__main__":
    Base.metadata.create_all(bind=engine)
    session = SessionLocal()
    # очистка для демонстрации:
    session.query(Student).delete()
    session.query(Group).delete()
    session.commit()

    g1 = Group(name="CS-01")
    g2 = Group(name="DS-01")
    session.add_all([g1, g2])
    session.commit()

    s1 = Student(name="Nurbek", age=20, group_id=g1.id)
    s2 = Student(name="Ilyas", age=21, group_id=g1.id)
    s3 = Student(name="Samat", age=22, group_id=g2.id)
    session.add_all([s1, s2, s3])
    session.commit()
    session.close()
    print("Seed created.")
