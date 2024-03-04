SELECT Subjects.name
FROM Subjects
JOIN Teachers ON Subjects.id_teacher = Teachers.id
WHERE Teachers.name = 'Sherri French'; -- change
