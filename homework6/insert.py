import sqlite3
from faker import Faker
import random

fake = Faker()

with sqlite3.connect("database.db") as db:
    cursor = db.cursor()

    for _ in range(5): 
        group_name = fake.company() 
        cursor.execute("INSERT INTO Groups (name) VALUES (?)", (group_name,))
    
    for _ in range(5):  
        teacher_name = fake.name()  
        cursor.execute("INSERT INTO Teachers (name) VALUES (?)", (teacher_name,))

    for _ in range(10):
        subject_name = fake.word()
        teacher_id = random.randint(1, 5)  
        cursor.execute("INSERT INTO Subjects (name, id_teacher) VALUES (?, ?)", (subject_name, teacher_id))

    for _ in range(20):
        student_name = fake.name() 
        group_id = random.randint(1, 5)  
        cursor.execute("INSERT INTO Students (name, id_group) VALUES (?, ?)", (student_name, group_id))

    for _ in range(50):
        mark_value = random.randint(2, 5) 
        mark_date = fake.date_time_between(start_date='-1y', end_date='now') 
        cursor.execute("INSERT INTO Marks (mark, date) VALUES (?, ?)", (mark_value, mark_date))

    for student_id in range(1, 21): 
        for _ in range(3): 
            subject_id = random.randint(1, 10)  
            mark_id = random.randint(1, 50) 
            cursor.execute("INSERT INTO Data (id_student, id_mark, id_subject) VALUES (?, ?, ?)", (student_id, mark_id, subject_id))
