from flask import Flask, render_template, request, redirect, url_for, send_from_directory
import sqlite3

app = Flask(
    __name__,
    static_folder="static",
    static_url_path="/static"
)

# ---------------- DATABASE ----------------

def get_db_connection():
    conn = sqlite3.connect("college_events.db")
    conn.row_factory = sqlite3.Row
    return conn


def create_database():

    conn = get_db_connection()

    # Students table
    conn.execute("""
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            phone TEXT,
            course TEXT,
            year TEXT
        )
    """)

    # Events table
    conn.execute("""
        CREATE TABLE IF NOT EXISTS events (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            date TEXT NOT NULL,
            time TEXT NOT NULL,
            venue TEXT NOT NULL,
            description TEXT
        )
    """)

    # Admin table
    conn.execute("""
        CREATE TABLE IF NOT EXISTS admins (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            password TEXT NOT NULL
        )
    """)

    # Create default admin
    admin = conn.execute(
        "SELECT * FROM admins WHERE username = ?",
        ("admin",)
    ).fetchone()

    if admin is None:
        conn.execute(
            "INSERT INTO admins (username, password) VALUES (?, ?)",
            ("admin", "admin123")
        )

    conn.commit()
    conn.close()


# ---------------- HOME ----------------

@app.route("/")
def home():
    return render_template("index.html")


# ---------------- STUDENT REGISTRATION ----------------

@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        name = request.form["name"]
        email = request.form["email"]
        phone = request.form["phone"]
        course = request.form["course"]
        year = request.form["year"]

        conn = get_db_connection()

        conn.execute("""
            INSERT INTO students
            (name, email, phone, course, year)
            VALUES (?, ?, ?, ?, ?)
        """, (name, email, phone, course, year))

        conn.commit()
        conn.close()

        return """
        <h2>Registration Successful!</h2>
        <p>Student registered successfully.</p>
        <a href="/">Go to Home</a>
        """

    return render_template("register.html")


# ---------------- EVENTS ----------------

@app.route("/events")
def events():

    conn = get_db_connection()

    events = conn.execute(
        "SELECT * FROM events"
    ).fetchall()

    conn.close()

    return render_template(
        "events.html",
        events=events
    )


# ---------------- ADMIN LOGIN ----------------

@app.route("/admin", methods=["GET", "POST"])
def admin_login():

    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]

        conn = get_db_connection()

        admin = conn.execute(
            """
            SELECT * FROM admins
            WHERE username = ? AND password = ?
            """,
            (username, password)
        ).fetchone()

        conn.close()

        if admin:
            return redirect("/admin/dashboard")

        return render_template(
            "admin_login.html",
            error="Invalid username or password"
        )

    return render_template("admin_login.html")
@app.route("/add_event", methods=["GET", "POST"])
def add_event():
    if request.method == "POST":
        name = request.form["name"]
        date = request.form["date"]
        time = request.form["time"]
        venue = request.form["venue"]

        conn = get_db_connection()

        conn.execute(
            "INSERT INTO events (name, date, time, venue) VALUES (?, ?, ?, ?)",
            (name, date, time, venue)
        )

        conn.commit()
        conn.close()

        return redirect("/events")

    return render_template("add_event.html")
# ---------------- ADMIN DASHBOARD ----------------

@app.route("/admin/dashboard")
def admin_dashboard():

    conn = get_db_connection()

    students = conn.execute(
        "SELECT * FROM students"
    ).fetchall()

    events = conn.execute(
        "SELECT * FROM events"
    ).fetchall()

    conn.close()

    return render_template(
        "admin_dashboard.html",
        students=students,
        events=events
    )
@app.route("/delete_event/<int:event_id>")
def delete_event(event_id):
    conn = get_db_connection()

    conn.execute(
        "DELETE FROM events WHERE id = ?",
        (event_id,)
    )

    conn.commit()
    conn.close()
    return redirect("/admin/dashboard")
# ---------------- START APPLICATION ----------------

@app.route("/download-certificate")
def download_certificate():
    return send_from_directory(
        "certificates",
        "Nidhi_Kamble_Certificate.pdf",
        as_attachment=True
    )


if __name__ == "__main__":
    create_database()
    app.run(debug=True)