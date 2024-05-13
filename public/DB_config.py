from typing import List

DB_HOST = "localhost"
DB_USER = "root"
DB_PASSWORD = "root"

DB_NAME = "project"

# -------------------- query for db and tables


Create_DB = f"CREATE DATABASE IF NOT EXISTS {DB_NAME}"

Clean_data = f"""
DROP DATABASE {DB_NAME}
"""

Student_table = """
CREATE TABLE IF NOT EXISTS student (
  id VARCHAR(15) NOT NULL UNIQUE,
  
  ROLL INT AUTO_INCREMENT PRIMARY KEY,
  EMAIL VARCHAR(30) NOT NULL UNIQUE,
  NAME CHAR(30),
  PHONE VARCHAR(10),
  DEPARTMENT CHAR(20),
  SEMESTER CHAR(20),
  DOB DATE,
  GENDER CHAR(20),
  PASSWORD VARCHAR(30) NOT NULL,
  SECRET_QUESTION CHAR(30) NOT NULL,
  SECRET_ANSWER CHAR(30) NOT NULL, 
  
  created_at_time TIME DEFAULT (CURRENT_TIME),
  created_at_date DATE DEFAULT (CURRENT_DATE) 
)
"""

Teacher_table = """
CREATE TABLE IF NOT EXISTS teacher (
  id VARCHAR(15) PRIMARY KEY,
  
  NAME CHAR(50),
  EMAIL VARCHAR(30) NOT NULL UNIQUE,
  PASSWORD VARCHAR(30) NOT NULL,
  GENDER CHAR(10),
  DEPARTMENT CHAR(10),
  SECRET_QUESTION CHAR(40) NOT NULL,
  SECRET_ANSWER CHAR(50) NOT NULL,
    
  created_at_time TIME DEFAULT (CURRENT_TIME),
  created_at_date DATE DEFAULT (CURRENT_DATE)
)
"""

Attendance_table = """
CREATE TABLE IF NOT EXISTS attendance (
  id INT AUTO_INCREMENT PRIMARY KEY,
  
  student_id VARCHAR(15) NOT NULL DEFAULT 'unknown',
    
  FOREIGN KEY (student_id) REFERENCES student(id) ON DELETE SET DEFAULT,
    
  created_at_time TIME DEFAULT (CURRENT_TIME),
  created_at_date DATE DEFAULT (CURRENT_DATE)
)
"""

FACE_mapping = """
CREATE TABLE IF NOT EXISTS face_mapping (
  id INT AUTO_INCREMENT PRIMARY KEY,

  student_id VARCHAR(15) NOT NULL UNIQUE DEFAULT 'unknown',

  FOREIGN KEY (student_id) REFERENCES student(id) ON DELETE SET DEFAULT,

  created_at_time TIME DEFAULT (CURRENT_TIME),
  created_at_date DATE DEFAULT (CURRENT_DATE)
)
"""

CREATE_TABLE = [
    Student_table,
    Teacher_table,
    Attendance_table,
    FACE_mapping
    ]

