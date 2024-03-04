SELECT Subjects.name
FROM Subjects
JOIN Data ON Subjects.id = Data.id_subject
JOIN Students ON Data.id_student = Students.id
WHERE Students.id = 4; -- change
