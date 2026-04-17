import pymysql
from dotenv import load_dotenv
import os

load_dotenv()

conn = pymysql.connect(
    host=os.getenv("DB_HOST"),
    port=int(os.getenv("DB_PORT", 3306)),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    database=os.getenv("DB_NAME"),
)

cur = conn.cursor()

# Create tables
cur.execute("""
CREATE TABLE IF NOT EXISTS department (
    dept_name   VARCHAR(20) PRIMARY KEY,
    building    VARCHAR(15),
    budget      DECIMAL(12,2)
)
""")

cur.execute("""
CREATE TABLE IF NOT EXISTS student (
    ID          VARCHAR(5) PRIMARY KEY,
    name        VARCHAR(20) NOT NULL,
    dept_name   VARCHAR(20),
    tot_cred    DECIMAL(3,0),
    FOREIGN KEY (dept_name) REFERENCES department(dept_name)
)
""")

cur.execute("""
CREATE TABLE IF NOT EXISTS course (
    course_id   VARCHAR(8) PRIMARY KEY,
    title       VARCHAR(50),
    dept_name   VARCHAR(20),
    credits     DECIMAL(2,0),
    FOREIGN KEY (dept_name) REFERENCES department(dept_name)
)
""")

cur.execute("""
CREATE TABLE IF NOT EXISTS takes (
    ID          VARCHAR(5),
    course_id   VARCHAR(8),
    sec_id      VARCHAR(8),
    semester    VARCHAR(6),
    year        DECIMAL(4,0),
    grade       VARCHAR(2),
    PRIMARY KEY (ID, course_id, sec_id, semester, year),
    FOREIGN KEY (ID) REFERENCES student(ID),
    FOREIGN KEY (course_id) REFERENCES course(course_id)
)
""")

# Insert departments
cur.execute("DELETE FROM takes")
cur.execute("DELETE FROM student")
cur.execute("DELETE FROM course")
cur.execute("DELETE FROM department")

departments = [
    ("Comp. Sci.", "Taylor", 100000),
    ("Biology",    "Watson", 90000),
    ("Elec. Eng.", "Taylor", 85000),
    ("Finance",    "Painter", 120000),
    ("History",    "Painter", 50000),
    ("Music",      "Packard", 80000),
    ("Physics",    "Watson", 70000),
]
cur.executemany("INSERT INTO department VALUES (%s, %s, %s)", departments)

# Insert courses
courses = [
    ("CS-101",  "Intro. to Computer Science", "Comp. Sci.", 4),
    ("CS-190",  "Game Design",                "Comp. Sci.", 4),
    ("CS-315",  "Robotics",                   "Comp. Sci.", 3),
    ("CS-319",  "Image Processing",           "Comp. Sci.", 3),
    ("CS-347",  "Database System Concepts",   "Comp. Sci.", 3),
    ("EE-181",  "Intro. to Digital Systems",  "Elec. Eng.", 3),
    ("FIN-201", "Investment Banking",         "Finance",    3),
    ("HIS-351", "World History",              "History",    3),
    ("MU-199",  "Music Video Production",     "Music",      3),
    ("PHY-101", "Physical Principles",        "Physics",    4),
    ("BIO-101", "Intro. to Biology",          "Biology",    4),
    ("BIO-301", "Genetics",                   "Biology",    4),
]
cur.executemany("INSERT INTO course VALUES (%s, %s, %s, %s)", courses)

# Insert students
students = [
    ("00128", "Zhang",     "Comp. Sci.", 102),
    ("12345", "Shankar",   "Comp. Sci.", 32),
    ("19991", "Brandt",    "History",    80),
    ("23121", "Chavez",    "Finance",    110),
    ("44553", "Peltier",   "Physics",    56),
    ("45678", "Levy",      "Physics",    46),
    ("54321", "Williams",  "Comp. Sci.", 54),
    ("55739", "Sanchez",   "Music",      38),
    ("70557", "Snow",      "Physics",    0),
    ("76543", "Brown",     "Comp. Sci.", 58),
    ("76653", "Aoi",       "Elec. Eng.", 60),
    ("98765", "Bouchard",  "Elec. Eng.", 98),
    ("98988", "Tanaka",    "Biology",    120),
]
cur.executemany("INSERT INTO student VALUES (%s, %s, %s, %s)", students)

# Insert takes records
takes = [
    ("00128", "CS-101",  "1", "Fall",   2017, "A"),
    ("00128", "CS-347",  "1", "Fall",   2017, "A-"),
    ("12345", "CS-101",  "1", "Fall",   2017, "C"),
    ("12345", "CS-190",  "2", "Spring", 2017, "A"),
    ("12345", "CS-315",  "1", "Spring", 2018, "A"),
    ("12345", "CS-347",  "1", "Fall",   2017, "A"),
    ("19991", "HIS-351", "1", "Spring", 2018, "B"),
    ("19991", "MU-199",  "1", "Spring", 2018, "A-"),
    ("23121", "FIN-201", "1", "Spring", 2019, "B+"),
    ("44553", "PHY-101", "1", "Fall",   2017, "B-"),
    ("45678", "CS-101",  "1", "Fall",   2017, "F"),
    ("45678", "CS-101",  "1", "Spring", 2018, "B+"),
    ("45678", "CS-319",  "1", "Spring", 2018, "B"),
    ("54321", "CS-101",  "1", "Fall",   2017, "A-"),
    ("54321", "CS-190",  "2", "Spring", 2017, "B+"),
    ("55739", "MU-199",  "1", "Spring", 2018, "A"),
    ("76543", "CS-101",  "1", "Fall",   2017, "A"),
    ("76543", "CS-319",  "2", "Spring", 2018, "A"),
    ("76653", "EE-181",  "1", "Spring", 2017, "C"),
    ("98765", "CS-101",  "1", "Fall",   2017, "C-"),
    ("98765", "CS-315",  "1", "Spring", 2018, "B"),
    ("98988", "BIO-101", "1", "Summer", 2017, "A"),
    ("98988", "BIO-301", "1", "Summer", 2018, "A"),
    ("98988", "CS-190",  "2", "Spring", 2017, "A"),
]
cur.executemany(
    "INSERT INTO takes VALUES (%s, %s, %s, %s, %s, %s)", takes
)

conn.commit()
cur.close()
conn.close()
print("Database setup complete!")
