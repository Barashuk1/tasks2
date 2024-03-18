from sqlalchemy import create_engine, Column, Integer, String, Date, ForeignKey, select, Text, and_, desc, func
from sqlalchemy.orm import declarative_base, sessionmaker, Mapped, mapped_column, relationship

# docker run --name db -e POSTGRES_PASSWORD=1 -p 5432:5432 -d postgres

# alembic init alembic
# alembic revision --autogenerate -m 'Init'

engine = create_engine('postgresql://postgres:1@localhost/postgres')
DBSession = sessionmaker(bind=engine)
session = DBSession()

Base = declarative_base()

class Groups(Base):
    __tablename__ = 'groups'
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String)

class Marks(Base):
    __tablename__ = 'marks'
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    mark: Mapped[int] = mapped_column(Integer)
    date: Mapped[Date] = mapped_column(Date) 

class Teachers(Base):
    __tablename__ = 'teachers'
    id: Mapped[int] = mapped_column(primary_key=True, active_history=True)
    name: Mapped[str] = mapped_column(String)

class Subjects(Base):
    __tablename__ = 'subjects'
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String)
    teacher_id: Mapped[str] = mapped_column('teacher_id', Integer, ForeignKey('teachers.id'))
    teacher: Mapped['Teachers'] = relationship(Teachers)

class Students(Base):
    __tablename__ = 'students'
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String)
    group_id: Mapped[str] = mapped_column('group_id', Integer, ForeignKey('groups.id'))
    group: Mapped['Groups'] = relationship(Groups)
    age: Mapped[int] = mapped_column(Integer)

class Data(Base):
    __tablename__ = 'data'
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    student_id: Mapped[str] = mapped_column('student_id', Integer, ForeignKey('students.id'))
    mark_id: Mapped[str] = mapped_column('mark_id', Integer, ForeignKey('marks.id'))
    subject_id: Mapped[str] = mapped_column('subject_id', Integer, ForeignKey('subjects.id'))
    student: Mapped['Students'] = relationship(Students)
    mark: Mapped['Marks'] = relationship(Marks)
    subject: Mapped['Subjects'] = relationship(Subjects)


Base.metadata.create_all(engine)