CREATE DATABASE IF NOT EXISTS gymdb;
USE gymdb;

CREATE TABLE IF NOT EXISTS membership_plan (
    plan_id INT AUTO_INCREMENT PRIMARY KEY,
    plan_name VARCHAR(30) NOT NULL UNIQUE,
    duration_months INT NOT NULL,
    cost DECIMAL(10, 2) NOT NULL
);

CREATE TABLE IF NOT EXISTS members (
    member_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    age INT,
    gender VARCHAR(10),
    contact VARCHAR(15) NOT NULL UNIQUE,
    join_date DATE NOT NULL,
    plan_id INT NOT NULL,
    FOREIGN KEY (plan_id) REFERENCES membership_plan(plan_id)
);

CREATE TABLE IF NOT EXISTS attendance (
    att_id INT AUTO_INCREMENT PRIMARY KEY,
    member_id INT NOT NULL,
    att_date DATE NOT NULL,
    status VARCHAR(10) NOT NULL,
    FOREIGN KEY (member_id) REFERENCES members(member_id),
    UNIQUE KEY unique_member_attendance (member_id, att_date)
);

CREATE TABLE IF NOT EXISTS payment (
    payment_id INT AUTO_INCREMENT PRIMARY KEY,
    member_id INT NOT NULL,
    amount DECIMAL(10, 2) NOT NULL,
    payment_date DATE NOT NULL,
    payment_method VARCHAR(20) NOT NULL,
    FOREIGN KEY (member_id) REFERENCES members(member_id)
);

INSERT INTO membership_plan (plan_name, duration_months, cost)
VALUES
    ('Monthly', 1, 1000.00),
    ('Quarterly', 3, 2500.00),
    ('Yearly', 12, 9000.00)
ON DUPLICATE KEY UPDATE
    duration_months = VALUES(duration_months),
    cost = VALUES(cost);

CREATE OR REPLACE VIEW dashboard_members AS
SELECT
    m.member_id AS ID,
    m.name AS Name,
    m.age AS Age,
    m.gender AS Gender,
    m.contact AS Contact,
    m.join_date AS `Join Date`,
    p.plan_name AS Plan,
    p.cost AS Charges,
    COALESCE(SUM(pay.amount), 0) AS `Total Paid`,
    GREATEST(p.cost - COALESCE(SUM(pay.amount), 0), 0) AS `Due Charges`,
    DATE_ADD(m.join_date, INTERVAL p.duration_months MONTH) AS `Due Date`,
    CASE
        WHEN COALESCE(SUM(pay.amount), 0) >= p.cost THEN 'Paid'
        ELSE 'Due'
    END AS Status
FROM members AS m
JOIN membership_plan AS p ON p.plan_id = m.plan_id
LEFT JOIN payment AS pay ON pay.member_id = m.member_id
GROUP BY m.member_id;

CREATE OR REPLACE VIEW dashboard AS
SELECT
    (SELECT COUNT(*) FROM members) AS total_members,
    (SELECT COUNT(*) FROM attendance
     WHERE att_date = CURRENT_DATE AND status = 'Present') AS present_today,
    (SELECT COALESCE(SUM(amount), 0) FROM payment) AS income;


