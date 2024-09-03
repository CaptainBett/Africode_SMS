# School Management System

## Overview

Welcome to the School Management System! This is a comprehensive web-based application developed using Flask. The system is designed to manage various aspects of a school, including student admissions, course management, performance tracking and more.

## Features

- **Student Management**: Handle student profiles and course enrollments.
- **Course Management**: Manage courses, and teachers. Students can view their enrolled courses and grades.
- **Performance Tracking**: Teachers can grade students, and students can view their grades and remarks.
- **User Roles**: Different roles for Admins, Teachers, and Students, with role-based access control.
- **Responsive UI**: Advanced Bootstrap styling ensures the application is fully responsive and user-friendly.

## Technology Stack

- **Backend**: Flask, Flask-SQLAlchemy ORM
- **Database**: PostgreSQL
- **Frontend**: HTML, CSS, Bootstrap
- **Security**: Flask-Security, role-based access control

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/CaptainBett/Africode_SMS
   cd school-management-system
   Set up a virtual environment:
   ```

bash
Copy code
python3 -m venv venv
source venv/bin/activate # On Windows use `venv\Scripts\activate`
Install the dependencies:

bash
Copy code
pip install -r requirements.txt
Set up the PostgreSQL database:

Create a new PostgreSQL database named school_management.
Update the config.py file with your database credentials.
Run database migrations:

bash
Copy code
flask db upgrade
Start the application:

bash
Copy code
flask run
Usage
Admin: Admins can manage courses, students, teachers, and the overall system.
Teacher: Teachers can manage their courses and grade students.
Student: Students can view their enrolled courses, grades.
Africode Academy
Africode Academy offers a wide range of coding courses designed to equip students with practical skills in web development, backend development, data science, and more. Africode Academy provides a strong foundation in coding principles and real-world projects to help students succeed in their tech careers.

License
This project is licensed under the MIT License. See the LICENSE file for more information.

Contributing
Contributions are welcome! If you'd like to contribute to this project, please submit a pull request or open an issue to discuss your ideas.
