SELECT DISTINCT Subjects.name
FROM Subjects
JOIN Data ON Subjects.id = Data.id_subject
JOIN Students ON Data.id_student = Students.id
JOIN Teachers ON Subjects.id_teacher = Teachers.id
WHERE Students.id = 4 AND Teachers.id = 4;
