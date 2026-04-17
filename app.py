from flask import Flask, render_template, request, redirect, url_for
import pymysql
import pymysql.cursors
import config

app = Flask(__name__)
app.secret_key = config.SECRET_KEY

def get_db():
    conn = pymysql.connect(
        host=config.DB_CONFIG["host"],
        port=config.DB_CONFIG["port"],
        user=config.DB_CONFIG["user"],
        password=config.DB_CONFIG["password"],
        database=config.DB_CONFIG["database"],
        cursorclass=pymysql.cursors.DictCursor
    )
    return conn

def get_departments():
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT dept_name FROM department ORDER BY dept_name")
    depts = cur.fetchall()
    conn.close()
    return depts

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/search", methods=["POST"])
def search():
    search_type = request.form.get("search_type")
    query = request.form.get("query", "").strip()

    if not query:
        return redirect(url_for("index"))

    pattern = "%" + query + "%"

    conn = get_db()
    cur = conn.cursor()

    if search_type == "name":
        cur.execute("SELECT ID, name, dept_name, tot_cred FROM student WHERE name LIKE %s", (pattern,))
    else:
        cur.execute("SELECT ID, name, dept_name, tot_cred FROM student WHERE ID LIKE %s", (pattern,))

    students = cur.fetchall()
    conn.close()

    return render_template("results.html", students=students, search_type=search_type, query=query)

@app.route("/add_student", methods=["GET", "POST"])
def add_student():
    if request.method == "GET":
        depts = get_departments()
        return render_template("add_student.html", departments=depts)

    # handle form submission
    sid = request.form.get("id", "").strip()
    name = request.form.get("name", "").strip()
    dept = request.form.get("dept_name", "").strip()
    is_transfer = request.form.get("is_transfer") == "on"
    credits = int(request.form.get("tot_cred", 0)) if is_transfer else 0

    if not sid or not name or not dept:
        depts = get_departments()
        return render_template("add_student.html", departments=depts, error="Please fill out all fields.")

    conn = get_db()
    cur = conn.cursor()
    try:
        cur.execute(
            "INSERT INTO student (ID, name, dept_name, tot_cred) VALUES (%s, %s, %s, %s)",
            (sid, name, dept, credits)
        )
        conn.commit()
    except pymysql.IntegrityError:
        conn.rollback()
        conn.close()
        depts = get_departments()
        return render_template("add_student.html", departments=depts, error=f"A student with ID {sid} already exists.")

    conn.close()
    return redirect(url_for("index"))

@app.route("/schedule/<student_id>")
def schedule(student_id):
    year = request.args.get("year", "")

    conn = get_db()
    cur = conn.cursor()

    cur.execute("SELECT ID, name FROM student WHERE ID = %s", (student_id,))
    student = cur.fetchone()

    if not student:
        conn.close()
        return render_template("schedule.html", student=None)

    cur.execute("SELECT DISTINCT year FROM takes WHERE ID = %s ORDER BY year DESC", (student_id,))
    years = [row["year"] for row in cur.fetchall()]

    if year:
        cur.execute("""
            SELECT t.ID, s.name, t.course_id, t.semester, t.year
            FROM takes t JOIN student s ON t.ID = s.ID
            WHERE t.ID = %s AND t.year = %s
            ORDER BY t.year DESC, t.semester
        """, (student_id, year))
    else:
        cur.execute("""
            SELECT t.ID, s.name, t.course_id, t.semester, t.year
            FROM takes t JOIN student s ON t.ID = s.ID
            WHERE t.ID = %s
            ORDER BY t.year DESC, t.semester
        """, (student_id,))

    rows = cur.fetchall()
    conn.close()

    return render_template("schedule.html", student=student, schedule=rows, years=years, selected_year=year)


if __name__ == "__main__":
    app.run(debug=config.DEBUG)
