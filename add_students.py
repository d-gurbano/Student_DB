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

new_students = [
    ("10001", "Johnson",   "Biology",    45),
    ("10002", "Martinez",  "Finance",    90),
    ("10003", "Nguyen",    "Comp. Sci.", 72),
    ("10004", "Patel",     "Elec. Eng.", 60),
    ("10005", "Robinson",  "History",    33),
    ("10006", "Kim",       "Music",      48),
    ("10007", "Garcia",    "Physics",    81),
    ("10008", "Johansson", "Finance",    110),
    ("10009", "Ali",       "Biology",    55),
    ("10010", "Chen",      "Comp. Sci.", 0),
    ("10011", "Okonkwo",   "History",    66),
    ("10012", "Petrov",    "Physics",    39),
    ("10013", "Lopez",     "Music",      27),
    ("10014", "Singh",     "Elec. Eng.", 93),
    ("10015", "Williams",  "Finance",    120),
    ("10016", "Nakamura",  "Biology",    84),
    ("10017", "Hassan",    "Comp. Sci.", 51),
    ("10018", "Andersen",  "History",    18),
    ("10019", "Ferreira",  "Physics",    63),
    ("10020", "Müller",    "Music",      75),
]

cur.executemany("INSERT IGNORE INTO student VALUES (%s, %s, %s, %s)", new_students)

new_takes = [
    # Johnson - Biology
    ("10001", "BIO-101", "1", "Fall",   2022, "B+"),
    ("10001", "BIO-301", "1", "Spring", 2023, "A"),
    # Martinez - Finance
    ("10002", "FIN-201", "1", "Fall",   2021, "A-"),
    ("10002", "CS-101",  "1", "Spring", 2022, "B"),
    # Nguyen - Comp. Sci.
    ("10003", "CS-101",  "1", "Fall",   2021, "A"),
    ("10003", "CS-190",  "2", "Spring", 2022, "A-"),
    ("10003", "CS-315",  "1", "Fall",   2022, "B+"),
    # Patel - Elec. Eng.
    ("10004", "EE-181",  "1", "Fall",   2021, "B"),
    ("10004", "CS-101",  "1", "Spring", 2022, "B+"),
    # Robinson - History
    ("10005", "HIS-351", "1", "Fall",   2022, "A"),
    # Kim - Music
    ("10006", "MU-199",  "1", "Spring", 2022, "A"),
    ("10006", "HIS-351", "1", "Fall",   2022, "B"),
    # Garcia - Physics
    ("10007", "PHY-101", "1", "Fall",   2021, "A-"),
    ("10007", "CS-101",  "1", "Spring", 2022, "B-"),
    ("10007", "EE-181",  "1", "Fall",   2022, "B+"),
    # Johansson - Finance
    ("10008", "FIN-201", "1", "Spring", 2020, "A"),
    ("10008", "CS-347",  "1", "Fall",   2021, "A-"),
    # Ali - Biology
    ("10009", "BIO-101", "1", "Fall",   2022, "B"),
    ("10009", "BIO-301", "1", "Spring", 2023, "B+"),
    # Chen - Comp. Sci. (new, no takes yet)
    # Okonkwo - History
    ("10011", "HIS-351", "1", "Fall",   2021, "A-"),
    ("10011", "MU-199",  "1", "Spring", 2022, "B+"),
    # Petrov - Physics
    ("10012", "PHY-101", "1", "Spring", 2023, "C+"),
    # Lopez - Music
    ("10013", "MU-199",  "1", "Fall",   2023, "A"),
    # Singh - Elec. Eng.
    ("10014", "EE-181",  "1", "Fall",   2020, "A"),
    ("10014", "CS-101",  "1", "Spring", 2021, "A-"),
    ("10014", "CS-315",  "1", "Fall",   2021, "B+"),
    ("10014", "CS-347",  "1", "Spring", 2022, "A"),
    # Williams - Finance (different from existing Williams)
    ("10015", "FIN-201", "1", "Fall",   2019, "B+"),
    ("10015", "CS-101",  "1", "Spring", 2020, "A"),
    ("10015", "CS-347",  "1", "Fall",   2020, "A-"),
    # Nakamura - Biology
    ("10016", "BIO-101", "1", "Fall",   2020, "A"),
    ("10016", "BIO-301", "1", "Spring", 2021, "A"),
    ("10016", "CS-190",  "2", "Fall",   2021, "B"),
    # Hassan - Comp. Sci.
    ("10017", "CS-101",  "1", "Fall",   2022, "B+"),
    ("10017", "CS-190",  "2", "Spring", 2023, "A-"),
    # Andersen - History
    ("10018", "HIS-351", "1", "Spring", 2024, "B"),
    # Ferreira - Physics
    ("10019", "PHY-101", "1", "Fall",   2022, "B"),
    ("10019", "EE-181",  "1", "Spring", 2023, "B+"),
    # Müller - Music
    ("10020", "MU-199",  "1", "Fall",   2021, "A"),
    ("10020", "HIS-351", "1", "Spring", 2022, "B+"),
    ("10020", "CS-190",  "2", "Fall",   2022, "B"),
]

cur.executemany("INSERT IGNORE INTO takes VALUES (%s, %s, %s, %s, %s, %s)", new_takes)

conn.commit()
cur.close()
conn.close()
print("Done! 20 students added.")
