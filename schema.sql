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