import sqlite3


with sqlite3.connect("D:/tasks2/homework6/database.db") as db:
    cursor = db.cursor()
    for i in range(1, 11):
        with open(file=f"query/query_{i}.sql", mode="r") as fr:
            query = fr.read()
            cursor.execute(query)

            results = cursor.fetchall()
            print(i, " | ", results)