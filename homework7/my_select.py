from sqlalchemy import func, join
from create_db import Data, Students, Subjects, Marks, Groups, Teachers
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

engine = create_engine('postgresql://postgres:1@localhost/postgres')
Session = sessionmaker(bind=engine)
session = Session()

def select_1(session):
    return session.query(Data.student_id, func.avg(Marks.mark).label('average_mark')) \
                    .join(Marks, Data.mark_id == Marks.id) \
                    .group_by(Data.student_id) \
                    .order_by(func.avg(Marks.mark).desc()) \
                    .limit(5) \
                    .all()

def select_2(session, subject_name):
    return session.query(Data.student_id, func.avg(Marks.mark).label('average_mark')) \
                    .join(Marks, Data.mark_id == Marks.id) \
                    .join(Subjects, Data.subject_id == Subjects.id) \
                    .filter(Subjects.name == subject_name) \
                    .group_by(Data.student_id) \
                    .order_by(func.avg(Marks.mark).desc()) \
                    .first()

def select_3(session, subject_name):
    return session.query(Groups.name, func.avg(Marks.mark).label('avg_mark')) \
                  .join(Students) \
                  .join(Data) \
                  .join(Marks) \
                  .join(Subjects) \
                  .filter(Subjects.name == subject_name) \
                  .group_by(Groups.id) \
                  .all()

def select_4(session):
    return session.query(Students.name, func.avg(Marks.mark).label('average_mark')) \
                    .join(Data, Students.id == Data.student_id) \
                    .join(Marks, Data.mark_id == Marks.id) \
                    .group_by(Students.name) \
                    .order_by(func.avg(Marks.mark).desc()) \
                    .limit(5) \
                    .all()

def select_5(session, teacher_name):
    return session.query(Subjects.name) \
                  .join(Teachers) \
                  .filter(Teachers.name == teacher_name) \
                  .all()

def select_6(session, group_id):
    return session.query(Students.name) \
                  .join(Groups) \
                  .filter(Groups.id == group_id) \
                  .all()

def select_7(session, group_id, subject_name):
    return session.query(Students.name, Marks.mark).\
        join(Data, Students.id == Data.student_id).\
        join(Marks, Data.mark_id == Marks.id).\
        join(Subjects, Data.subject_id == Subjects.id).\
        join(Groups, Students.group_id == Groups.id).\
        filter(Groups.id == group_id).\
        filter(Subjects.name == subject_name).\
        all()
            
def select_8(session, teacher_id):
    return session.query(Subjects.name, func.avg(Marks.mark).label('average_mark')
        ).join(Data, Subjects.id == Data.subject_id).\
        join(Marks, Data.mark_id == Marks.id).\
        join(Teachers, Subjects.teacher_id == Teachers.id).\
        filter(Teachers.id == teacher_id).\
        group_by(Subjects.name).all()

def select_9(session, student_name):
    return session.query(Subjects.name) \
                  .join(Data) \
                  .join(Students) \
                  .filter(Students.name == student_name) \
                  .all()

def select_10(session, student_name, teacher_name):
    return session.query(Subjects.name) \
                  .join(Data) \
                  .join(Students) \
                  .join(Teachers) \
                  .filter(Students.name == student_name) \
                  .filter(Teachers.name == teacher_name) \
                  .all()



if __name__ == '__main__':

    result_1 = select_1(session)
    print("Top 5 students with highest average marks:")
    for student, avg_mark in result_1:
        print(f"Student: {student}, Average Mark: {avg_mark}")
    
    print("#######################################################")

    result_2 = select_2(session, 'Math')
    print("Top student with highest average mark in Math:")
    if result_2 is not None:
        print(f"Student: {result_2[0]}, Average Mark: {result_2[1]}")
    else:
        print("No data found for the specified subject.")
        
    print("#######################################################")

    result_3 = select_3(session, 'Math')
    print(f"Average mark in Math: {result_3}")

    print("#######################################################")

    result_4 = select_4(session)
    for student_name, average_mark in result_4:
        print(f"Student: {student_name}, Average Mark: {average_mark}")

    print("#######################################################")

    result_5 = select_5(session, 'John Doe')
    print("Courses taught by John Doe:")
    for course in result_5:
        print(course)

    print("#######################################################")

    result_6 = select_6(session, 1)
    print("Students in Group 1:")
    for student in result_6:
        print(student)

    print("#######################################################")

    result_7 = select_7(session, 1, 'Math')
    print("Marks of students in Group 1 for Math:")
    for student, mark in result_7:
        print(f"Student: {student}, Mark: {mark}")
        
    print("#######################################################")
        
    result_8 = select_8(session, 1)
    print(f"Average mark given by Teacher 1: {result_8}")

    print("#######################################################")

    result_9 = select_9(session, 'Joe')
    print("Courses attended by Alice:")
    for course in result_9:
        print(course)

    print("#######################################################")

    result_10 = select_10(session, 'Alice', 'John Doe')
    print("Courses attended by Alice taught by John Doe:")
    for course in result_10:
        print(course)
