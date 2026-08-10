-- =====================================================
-- Course Database Design
-- Author: Pavlo Huz
-- MySQL
-- =====================================================


-- 1. Create a database for course management.

CREATE DATABASE IF NOT EXISTS courses;

USE courses;


-- Create teachers table.

CREATE TABLE IF NOT EXISTS teachers (
    teacher_no INT AUTO_INCREMENT,
    teacher_name VARCHAR(100) NOT NULL,
    phone_no VARCHAR(20),
    PRIMARY KEY (teacher_no)
);


-- Create courses table.

CREATE TABLE IF NOT EXISTS courses (
    course_no INT AUTO_INCREMENT,
    course_name VARCHAR(100) NOT NULL,
    start_date DATE NOT NULL,
    end_date DATE NOT NULL,
    PRIMARY KEY (course_no)
);


-- Create students table with foreign keys.

CREATE TABLE IF NOT EXISTS students (
    student_no INT AUTO_INCREMENT,
    teacher_no INT NOT NULL,
    course_no INT NOT NULL,
    student_name VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL,
    birth_date DATE NOT NULL,
    PRIMARY KEY (student_no),
    CONSTRAINT fk_teacher
        FOREIGN KEY (teacher_no)
        REFERENCES teachers(teacher_no),
    CONSTRAINT fk_course
        FOREIGN KEY (course_no)
        REFERENCES courses(course_no)
);


-- 2. Insert sample data into each table.

START TRANSACTION;

INSERT INTO teachers (teacher_name, phone_no)
VALUES
('John Smith', '+380501111111'),
('Emily Johnson', '+380502222222'),
('Michael Brown', '+380503333333'),
('Sophia Davis', '+380504444444'),
('Daniel Wilson', '+380505555555'),
('Olivia Martinez', '+380506666666'),
('James Anderson', '+380507777777'),
('Isabella Thomas', '+380508888888');


INSERT INTO courses (course_name, start_date, end_date)
VALUES
('SQL Basics', '2026-01-10', '2026-03-10'),
('Advanced SQL', '2026-02-01', '2026-04-01'),
('Power BI Fundamentals', '2026-01-15', '2026-03-15'),
('Excel for Analysts', '2026-02-10', '2026-04-10'),
('Database Design', '2026-03-01', '2026-05-01'),
('Python Basics', '2026-03-15', '2026-05-15'),
('Data Visualization', '2026-04-01', '2026-06-01'),
('Statistics for Data Analysis', '2026-04-10', '2026-06-10');


INSERT INTO students (
    teacher_no,
    course_no,
    student_name,
    email,
    birth_date
)
VALUES
(1, 1, 'Anna Ivanova', 'anna.ivanova@gmail.com', '2001-05-14'),
(2, 2, 'Petro Sydorenko', 'petro.sydorenko@gmail.com', '2000-08-22'),
(3, 3, 'Maria Kovalenko', 'maria.kovalenko@gmail.com', '2002-01-11'),
(4, 4, 'Oleg Martyniuk', 'oleg.martyniuk@gmail.com', '1999-11-03'),
(5, 5, 'Iryna Boiko', 'iryna.boiko@gmail.com', '2001-07-19'),
(6, 6, 'Dmytro Tkach', 'dmytro.tkach@gmail.com', '2003-04-27'),
(7, 7, 'Sofiia Levchenko', 'sofiia.levchenko@gmail.com', '2002-09-09'),
(8, 8, 'Vladyslav Romaniuk', 'vlad.romaniuk@gmail.com', '2000-12-30');

COMMIT;


-- Check inserted data.

SELECT *
FROM courses.teachers;

SELECT *
FROM courses.courses;

SELECT *
FROM courses.students;


-- 3. Show the number of students each teacher has worked with.

WITH teachers_students AS
(
    SELECT
        teacher_no,
        COUNT(student_no) AS count_of_students
    FROM courses.students
    GROUP BY teacher_no
)
SELECT
    tch.teacher_no,
    tch.teacher_name,
    ts.count_of_students
FROM teachers_students ts
INNER JOIN courses.teachers tch
    ON ts.teacher_no = tch.teacher_no;


-- 4. Create three duplicate rows in the students table.

INSERT INTO students (
    teacher_no,
    course_no,
    student_name,
    email,
    birth_date
)
SELECT
    teacher_no,
    course_no,
    student_name,
    email,
    birth_date
FROM students
LIMIT 3;


-- 5. Find duplicated rows in the students table.

WITH duplicated_rows AS
(
    SELECT
        teacher_no,
        course_no,
        student_name,
        email,
        birth_date
    FROM courses.students
    GROUP BY
        teacher_no,
        course_no,
        student_name,
        email,
        birth_date
    HAVING COUNT(*) > 1
)
SELECT
    std.*
FROM duplicated_rows dr
INNER JOIN courses.students std
    ON dr.teacher_no = std.teacher_no
    AND dr.course_no = std.course_no
    AND dr.student_name = std.student_name
    AND dr.email = std.email
    AND dr.birth_date = std.birth_date;
