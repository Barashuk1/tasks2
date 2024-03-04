import sqlite3

with sqlite3.connect("database.db") as db:
    cursor = db.cursor()
    query = """ 
        CREATE TABLE IF NOT EXISTS Groups(
            id INTEGER PRIMARY KEY AUTOINCREMENT, 
            name VARCHAR(255)
        ) """
    cursor.execute(query)

with sqlite3.connect("database.db") as db:
    cursor = db.cursor()
    query = """ 
        CREATE TABLE IF NOT EXISTS Marks(
            id INTEGER PRIMARY KEY AUTOINCREMENT, 
            mark INT,
            date DATE
        ) """
    cursor.execute(query)

with sqlite3.connect("database.db") as db:
    cursor = db.cursor()
    query = """ 
        CREATE TABLE IF NOT EXISTS Teachers(
            id INTEGER PRIMARY KEY AUTOINCREMENT, 
            name VARCHAR(255)
        ) """
    cursor.execute(query)

with sqlite3.connect("database.db") as db:
    cursor = db.cursor()
    query = """ 
        CREATE TABLE IF NOT EXISTS Subjects(
            id INTEGER PRIMARY KEY AUTOINCREMENT, 
            name VARCHAR(255),
            id_teacher INT REFERENCES Teachers(id)
        ) """
    cursor.execute(query)

with sqlite3.connect("database.db") as db:
    cursor = db.cursor()
    query = """ 
        CREATE TABLE IF NOT EXISTS Data(
            id INTEGER PRIMARY KEY AUTOINCREMENT, 
            id_student INT REFERENCES Students(id),
            id_mark INT REFERENCES Marks(id),
            id_subject INT REFERENCES Subjects(id)
        ) """
    cursor.execute(query)

with sqlite3.connect("database.db") as db:
    cursor = db.cursor()
    query = """ 
        CREATE TABLE IF NOT EXISTS Students(
            id INTEGER PRIMARY KEY AUTOINCREMENT, 
            name VARCHAR(255),
            id_group INT REFERENCES Groups(id)
        ) """
    cursor.execute(query)
