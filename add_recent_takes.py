import pymysql
from dotenv import load_dotenv
import os
import random

load_dotenv()

conn = pymysql.connect(
    host=os.getenv("DB_HOST"),
    port=int(os.getenv("DB_PORT", 3306)),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    database=os.getenv("DB_NAME"),
)
cur = conn.cursor()

# All students and their departments
students = [
    ("00128", "Comp. Sci."),
    ("10001", "Biology"),
    ("10002", "Finance"),
    ("10003", "Comp. Sci."),
    ("10004", "Elec. Eng."),
    ("10005", "History"),
    ("10006", "Music"),
    ("10007", "Physics"),
    ("10008", "Finance"),
    ("10009", "Biology"),
    ("10010", "Comp. Sci."),
    ("10011", "History"),
    ("10012", "Physics"),
    ("10013", "Music"),
    ("10014", "Elec. Eng."),
    ("10015", "Finance"),
    ("10016", "Biology"),
    ("10017", "Comp. Sci."),
    ("10018", "History"),
    ("10019", "Physics"),
    ("10020", "Music"),
    ("12345", "Comp. Sci."),
    ("19991", "History"),
    ("23121", "Finance"),
    ("44553", "Physics"),
    ("45678", "Physics"),
    ("54321", "Comp. Sci."),
    ("55739", "Music"),
    ("70557", "Physics"),
    ("76543", "Comp. Sci."),
    ("76653", "Elec. Eng."),
    ("98765", "Elec. Eng."),
    ("98988", "Biology"),
]

# Courses grouped by department + cross-dept electives
dept_courses = {
    "Comp. Sci.": ["CS-101", "CS-190", "CS-315", "CS-319", "CS-347"],
    "Biology":    ["BIO-101", "BIO-301"],
    "Finance":    ["FIN-201"],
    "Elec. Eng.": ["EE-181", "CS-101"],
    "History":    ["HIS-351", "MU-199"],
    "Music":      ["MU-199", "HIS-351"],
    "Physics":    ["PHY-101", "EE-181", "CS-101"],
}

# Cross-dept electives any student might take
electives = ["CS-101", "HIS-351", "MU-199", "PHY-101", "BIO-101"]

grades = ["A", "A-", "B+", "B", "B-", "C+", "C", "C-"]

# Semesters per year in order
schedule = [
    (2024, "Fall"),
    (2025, "Spring"),
    (2025, "Summer"),
    (2025, "Fall"),
    (2026, "Spring"),
    (2026, "Summer"),
    (2026, "Fall"),
]

takes = []

for student_id, dept in students:
    pool = dept_courses.get(dept, []) + random.sample(electives, k=2)
    pool = list(set(pool))  # deduplicate

    for (year, semester) in schedule:
        # pick 1-3 courses per semester
        num_courses = random.randint(1, min(3, len(pool)))
        chosen = random.sample(pool, k=num_courses)
        for course_id in chosen:
            grade = random.choice(grades)
            takes.append((student_id, course_id, "1", semester, year, grade))

# Deduplicate on (ID, course_id, sec_id, semester, year)
seen = set()
unique_takes = []
for t in takes:
    key = (t[0], t[1], t[2], t[3], t[4])
    if key not in seen:
        seen.add(key)
        unique_takes.append(t)

cur.executemany("INSERT IGNORE INTO takes VALUES (%s, %s, %s, %s, %s, %s)", unique_takes)
conn.commit()
print(f"Inserted {len(unique_takes)} takes records.")
cur.close()
conn.close()
