SELECT Groups.id, Groups.name, AVG(Marks.mark) AS average_mark
FROM Groups
JOIN Students ON Groups.id = Students.id_group
JOIN Data ON Students.id = Data.id_student
JOIN Marks ON Data.id_mark = Marks.id
JOIN Subjects ON Data.id_subject = Subjects.id
WHERE Subjects.name = 'some' -- change
GROUP BY Groups.id, Groups.name;
