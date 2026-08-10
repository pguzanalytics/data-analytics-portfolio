-- =====================================================
-- Employee & Salary Analysis
-- Author: Pavlo Huz
-- MySQL
-- =====================================================


-- 1. Show the average employee salary for each year before 2005.

SELECT
    YEAR(from_date) AS year_sal,
    ROUND(AVG(salary), 2) AS avg_sal
FROM employees.salaries
WHERE from_date < '2005-01-01'
GROUP BY YEAR(from_date)
ORDER BY year_sal;


-- 2. Show the average current salary for each department.
-- Only current salaries and current department assignments are included.

SELECT
    dept.dept_no,
    ROUND(AVG(sal.salary), 2) AS avg_sal
FROM employees.dept_emp dept
INNER JOIN employees.salaries sal
    ON dept.emp_no = sal.emp_no
WHERE sal.to_date > CURDATE()
    AND dept.to_date > CURDATE()
GROUP BY dept.dept_no
ORDER BY dept.dept_no;


-- 3. Show the average employee salary for each department by year.

SELECT
    dept.dept_no,
    YEAR(sal.from_date) AS sal_year,
    ROUND(AVG(sal.salary), 2) AS avg_sal
FROM employees.dept_emp dept
INNER JOIN employees.salaries sal
    ON dept.emp_no = sal.emp_no
WHERE sal.from_date >= dept.from_date
    AND sal.from_date <= dept.to_date
GROUP BY dept.dept_no, sal_year
ORDER BY dept.dept_no, sal_year;


-- 4. Show departments that currently have more than 15,000 employees.

SELECT
    dept_no,
    COUNT(DISTINCT emp_no) AS count_of_emp
FROM employees.dept_emp
WHERE to_date > CURDATE()
GROUP BY dept_no
HAVING count_of_emp > 15000;


-- 5. Show the employee number, department, hire date,
-- and last name of the longest-serving current manager.

WITH current_managers AS
(
    SELECT
        emp_no,
        dept_no
    FROM employees.dept_manager
    WHERE to_date > CURDATE()
),
info_of_current_managers AS
(
    SELECT
        cm.emp_no,
        cm.dept_no,
        emp.hire_date,
        emp.last_name
    FROM current_managers cm
    INNER JOIN employees.employees emp
        ON cm.emp_no = emp.emp_no
)
SELECT
    emp_no,
    dept_no,
    hire_date,
    last_name
FROM info_of_current_managers
WHERE hire_date =
(
    SELECT MIN(hire_date)
    FROM info_of_current_managers
);


-- 6. Show the Top 10 current employees with the largest difference
-- between their salary and the average salary in their department.

WITH avg_sal_of_dept AS
(
    SELECT
        dept.dept_no,
        ROUND(AVG(sal.salary), 2) AS avg_sal
    FROM employees.dept_emp dept
    INNER JOIN employees.salaries sal
        ON dept.emp_no = sal.emp_no
    WHERE sal.to_date > CURDATE()
        AND dept.to_date > CURDATE()
    GROUP BY dept.dept_no
),
current_sal AS
(
    SELECT
        sal.emp_no,
        sal.salary,
        dept.dept_no,
        asd.avg_sal
    FROM employees.salaries sal
    INNER JOIN employees.dept_emp dept
        ON dept.emp_no = sal.emp_no
    INNER JOIN avg_sal_of_dept asd
        ON asd.dept_no = dept.dept_no
    WHERE sal.to_date > CURDATE()
        AND dept.to_date > CURDATE()
)
SELECT
    emp_no,
    dept_no,
    salary,
    avg_sal,
    ABS(salary - avg_sal) AS diff_salary
FROM current_sal
ORDER BY diff_salary DESC
LIMIT 10;


-- 7. Show the second manager in chronological order for each department.
-- Return department, manager name, hire date, and manager start date.

WITH managers_rank AS
(
    SELECT
        emp_no,
        dept_no,
        from_date,
        ROW_NUMBER() OVER (
            PARTITION BY dept_no
            ORDER BY from_date
        ) AS rank_of_manager
    FROM employees.dept_manager
)
SELECT
    mr.dept_no,
    CONCAT(emp.first_name, ' ', emp.last_name) AS full_name,
    emp.hire_date,
    mr.from_date AS manager_from_date
FROM managers_rank mr
INNER JOIN employees.employees emp
    ON mr.emp_no = emp.emp_no
WHERE mr.rank_of_manager = 2
ORDER BY mr.dept_no, manager_from_date;
