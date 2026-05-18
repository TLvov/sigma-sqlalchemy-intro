DROP TABLE student_course;
DROP TABLE student;
DROP TABLE course;
DROP TABLE lecturer;

CREATE TABLE lecturer (
    lecturer_id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    lecturer_name VARCHAR(30) NOT NULL
);

CREATE TABLE course (
    course_id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    course_title VARCHAR(30) UNIQUE NOT NULL,
    lecturer_id INT REFERENCES lecturer(lecturer_id)
);

CREATE TABLE student (
    student_id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    student_name VARCHAR(30)
);

CREATE TABLE student_course (
    student_course_id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    course_id INT REFERENCES course(course_id),
    student_id INT REFERENCES student(student_id)
);