SELECT Students.id, Students.name, AVG(Marks.mark) AS average_mark
FROM Students
JOIN Data ON Students.id = Data.id_student
JOIN Marks ON Data.id_mark = Marks.id
GROUP BY Students.id, Students.name
ORDER BY average_mark DESC
LIMIT 5;