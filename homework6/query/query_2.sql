SELECT Students.id, Students.name, AVG(Marks.mark) AS average_mark
FROM Students
JOIN Data ON Students.id = Data.id_student
JOIN Marks ON Data.id_mark = Marks.id
JOIN Subjects ON Data.id_subject = Subjects.id
WHERE Subjects.name = 'some' -- change
GROUP BY Students.id, Students.name
ORDER BY average_mark DESC
LIMIT 1;
