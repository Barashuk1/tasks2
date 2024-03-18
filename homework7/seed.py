from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from faker import Faker
from datetime import datetime, timedelta
from create_db import Students, Groups, Teachers, Subjects, Marks, Data
from random import randint, choice

engine = create_engine('postgresql://postgres:1@localhost/postgres')
Session = sessionmaker(bind=engine)
session = Session()

fake = Faker()

groups = [Groups(name=f"Group {i}") for i in range(1, 4)]
session.add_all(groups)
session.commit()

teachers = [Teachers(name=fake.name()) for _ in range(5)]
session.add_all(teachers)
session.commit()

subjects = [Subjects(name=fake.word(), teacher_id=choice(teachers).id) for _ in range(8)]
session.add_all(subjects)
session.commit()

students = [Students(name=fake.name(), group_id=choice(groups).id, age=randint(18, 25)) for _ in range(50)]
session.add_all(students)
session.commit()

for student in students:
    for subject in subjects:
        mark_value = randint(60, 100)
        date = fake.date_between(start_date='-30d', end_date='today')
        mark = Marks(mark=mark_value, date=date)
        session.add(mark)
        session.commit()
        data = Data(student_id=student.id, subject_id=subject.id, mark_id=mark.id)
        session.add(data)

session.commit()
session.close()
