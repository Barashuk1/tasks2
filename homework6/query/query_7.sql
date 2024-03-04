SELECT Students.name, Marks.mark
FROM Students
JOIN Data ON Students.id = Data.id_student
JOIN Marks ON Data.id_mark = Marks.id
JOIN Subjects ON Data.id_subject = Subjects.id
WHERE Students.id_group = 4 AND Subjects.name = 'some';
