# Gym Management System

A desktop-based **Gym Management System** built with Python, Tkinter,
and MySQL. It helps gym staff manage member registrations, daily
attendance, membership payments, and dashboard summaries.

## Features

-   Register members with name, age, gender, contact number, joining
    date, and membership plan.
-   Mark daily attendance as Present or Absent.
-   Prevent duplicate attendance entries for the same member on the same
    date.
-   Record payments using Cash, Card, or UPI.
-   View member charges, total paid, due charges, due date, and payment
    status.
-   View total members, members present today, and total recorded
    income.

## Tech Stack

-   Python 3
-   Tkinter / ttk
-   MySQL
-   `mysql-connector-python`
-   `Pillow`

## Project Structure

``` text
gym-management-system/
├── gym.py
├── requirements.txt
├── sql_query+project.sql
├── assets/
│   └── gym_header.png
└── README.md
```

**Important:** The application expects `assets/gym_header.png` to exist.
Create the `assets` folder and add your header image there.

## Prerequisites

-   Python 3
-   MySQL Server
-   pip

## Installation

### 1. Clone the repository

``` bash
git clone https://github.com/YOUR-USERNAME/YOUR-REPOSITORY.git
cd YOUR-REPOSITORY
```

Replace the URL and folder name with your repository details.

### 2. Install dependencies

``` bash
pip install -r requirements.txt
```

### 3. Set up the MySQL database

Start MySQL, open MySQL Workbench (or another MySQL client), and execute
`sql_query+project.sql`.

The script creates the `gymdb` database, four tables (`membership_plan`,
`members`, `attendance`, and `payment`), and two dashboard views
(`dashboard_members` and `dashboard`). It also inserts Monthly,
Quarterly, and Yearly membership plans.

### 4. Configure the database connection

Update the connection settings inside `connect_db()` in `gym.py` to
match your local MySQL configuration:

``` python
return mysql.connector.connect(
    host="localhost",
    user="YOUR_MYSQL_USERNAME",
    password="YOUR_MYSQL_PASSWORD",
    database="gymdb"
)
```

**Security:** Never publish your real MySQL password in a public
repository. Use environment variables or a local configuration file
excluded through `.gitignore`.

### 5. Add the header image

Place your image at:

``` text
assets/gym_header.png
```

### 6. Run the application

``` bash
python gym.py
```

## How to Use

1.  Run the application.
2.  Choose **Add Member** to register a member and select a membership
    plan.
3.  Choose **Mark Attendance** to record today's attendance.
4.  Choose **Payments** to record a payment.
5.  Choose **Dashboard** to review member information and summary
    totals.

## Database Overview

  Table / View          Purpose
  --------------------- -----------------------------------------------
  `membership_plan`     Membership plan names, durations, and costs
  `members`             Member details and selected plan
  `attendance`          Daily attendance records
  `payment`             Member payment records
  `dashboard_members`   Member, plan, and payment summary
  `dashboard`           Overall member, attendance, and income totals

## Current Scope

This is a local desktop application configured to connect to MySQL on
`localhost`. It is a project/demo application and does not currently
include online hosting, user login, or role-based access control.

## Future Improvements

-   Add member search, update, and delete functionality.
-   Add date-wise attendance and revenue reports.
-   Add membership renewal and expiry notifications.
-   Add user authentication and role-based access.
-   Use environment variables for database credentials.
-   Add automated database backups.

## Author

**Your Name** --- replace this with your name and GitHub profile.

## License

No license is currently specified. Add a `LICENSE` file if you want to
define how others may use, modify, or distribute this project.
