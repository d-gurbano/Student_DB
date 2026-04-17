import pymysql
import pymysql.cursors
from flask import Flask, render_template, request, redirect, url_for
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
        cursorclass=pymysql.cursors.DictCursor,
    )
    return conn


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/search", methods=["POST"])
def search():
    search_type = request.form.get("search_type")
    query_str = request.form.get("query", "").strip()

    if not query_str:
        return redirect(url_for("index"))

    pattern = f"%{query_str}%"

    if search_type == "name":
        sql = "SELECT ID, name, dept_name, tot_cred FROM student WHERE name LIKE %s"
    else:
        sql = "SELECT ID, name, dept_name, tot_cred FROM student WHERE ID LIKE %s"

    conn = get_db()
    try:
        with conn.cursor() as cur:
            cur.execute(sql, (pattern,))
            students = cur.fetchall()
    finally:
        conn.close()

    return render_template(
        "results.html",
        students=students,
        search_type=search_type,
        query=query_str,
    )


@app.route("/add_student")
def add_student():
    conn = get_db()
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT dept_name FROM department ORDER BY dept_name")
            departments = cur.fetchall()
    finally:
        conn.close()
    return render_template("add_student.html", departments=departments)


@app.route("/add_student", methods=["POST"])
def add_student_submit():
    student_id   = request.form.get("id", "").strip()
    student_name = request.form.get("name", "").strip()
    dept_name    = request.form.get("dept_name", "").strip()
    is_transfer  = request.form.get("is_transfer") == "on"
    tot_cred     = int(request.form.get("tot_cred", 0)) if is_transfer else 0

    def reload_form(error):
        conn2 = get_db()
        try:
            with conn2.cursor() as cur2:
                cur2.execute("SELECT dept_name FROM department ORDER BY dept_name")
                departments = cur2.fetchall()
        finally:
            conn2.close()
        return render_template("add_student.html", departments=departments, error=error)

    if not student_id or not student_name or not dept_name:
        return reload_form("All fields are required.")

    conn = get_db()
    try:
        with conn.cursor() as cur:
            cur.execute(
                "INSERT INTO student (ID, name, dept_name, tot_cred) VALUES (%s, %s, %s, %s)",
                (student_id, student_name, dept_name, tot_cred),
            )
        conn.commit()
    except pymysql.IntegrityError:
        conn.rollback()
        return reload_form(f"Student ID '{student_id}' already exists.")
    finally:
        conn.close()

    return redirect(url_for("index"))


@app.route("/schedule/<student_id>")
def schedule(student_id):
    year_filter = request.args.get("year", "").strip()

    conn = get_db()
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT ID, name FROM student WHERE ID = %s", (student_id,))
            student = cur.fetchone()

            if not student:
                return render_template("schedule.html", student=None)

            cur.execute(
                "SELECT DISTINCT year FROM takes WHERE ID = %s ORDER BY year DESC",
                (student_id,),
            )
            years = [row["year"] for row in cur.fetchall()]

            if year_filter:
                cur.execute(
                    """
                    SELECT t.ID, s.name, t.course_id, t.semester, t.year
                    FROM takes t
                    JOIN student s ON t.ID = s.ID
                    WHERE t.ID = %s AND t.year = %s
                    ORDER BY t.year DESC, t.semester
                    """,
                    (student_id, year_filter),
                )
            else:
                cur.execute(
                    """
                    SELECT t.ID, s.name, t.course_id, t.semester, t.year
                    FROM takes t
                    JOIN student s ON t.ID = s.ID
                    WHERE t.ID = %s
                    ORDER BY t.year DESC, t.semester
                    """,
                    (student_id,),
                )
            schedule_rows = cur.fetchall()

    finally:
        conn.close()

    return render_template(
        "schedule.html",
        student=student,
        schedule=schedule_rows,
        years=years,
        selected_year=year_filter,
    )


if __name__ == "__main__":
    app.run(debug=config.DEBUG)
