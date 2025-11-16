from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from models import Group, Student, Teacher, Subject, Grade, Base
from faker import Faker
import random
from datetime import datetime

fake = Faker()

engine = create_engine("postgresql://postgres:mysecretpassword@localhost:5432/postgres")
Session = sessionmaker(bind=engine)
session = Session()

def seed():
    groups = []
    for name in ["A-101", "B-202", "C-303"]:
        group = Group(name=name)
        session.add(group)
        groups.append(group)

    teachers = []
    for _ in range(4):
        t = Teacher(fullname=fake.name())
        session.add(t)
        teachers.append(t)

  
    subjects = []
    subject_names = ["Math", "History", "Biology", "Physics", "Chemistry", "English"]
    for name in subject_names:
        s = Subject(name=name, teacher=random.choice(teachers))
        session.add(s)
        subjects.append(s)


    students = []
    for _ in range(40):
        st = Student(fullname=fake.name(), group=random.choice(groups))
        session.add(st)
        students.append(st)

    session.commit()


    for student in students:
        for subject in subjects:
            for _ in range(random.randint(5, 20)):
                g = Grade(
                    grade=random.randint(1, 12),
                    student=student,
                    subject=subject,
                    date_of=fake.date_time_between(start_date="-2y")
                )
                session.add(g)

    session.commit()


if __name__ == "__main__":
    seed()

