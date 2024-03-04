SELECT Teachers.name, AVG(Marks.mark) AS average_mark
FROM Teachers
JOIN Subjects ON Teachers.id = Subjects.id_teacher
JOIN Data ON Subjects.id = Data.id_subject
JOIN Marks ON Data.id_mark = Marks.id
GROUP BY Teachers.name;
