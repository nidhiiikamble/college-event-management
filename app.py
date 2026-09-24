from flask import Flask, render_template, request, redirect, url_for, session, send_file
import sqlite3
from io import BytesIO
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4


app = Flask(
    __name__,
    static_folder="static",
    static_url_path="/static"
)

# Secret key for student session
app.secret_key = "college-event-secret-key"


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

        # Save student's name in session
        session["student_name"] = name

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


# ---------------- ADD EVENT ----------------

@app.route("/add_event", methods=["GET", "POST"])
def add_event():

    if request.method == "POST":

        name = request.form["name"]
        date = request.form["date"]
        time = request.form["time"]
        venue = request.form["venue"]

        conn = get_db_connection()

        conn.execute(
            """
            INSERT INTO events
            (name, date, time, venue)
            VALUES (?, ?, ?, ?)
            """,
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


# ---------------- DELETE EVENT ----------------

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


# ---------------- DYNAMIC CERTIFICATE ----------------

@app.route("/download-certificate")
def download_certificate():

    # Get the currently registered student's name
    student_name = session.get("student_name")

    if not student_name:
        return """
        <h2>Please register first.</h2>
        <p>You need to register before downloading your certificate.</p>
        <a href="/register">Go to Registration</a>
        """

    # Create PDF in memory
    buffer = BytesIO()

    pdf = canvas.Canvas(buffer, pagesize=A4)

    width, height = A4

    # Certificate title
    pdf.setFont("Helvetica-Bold", 24)
    pdf.drawCentredString(
        width / 2,
        height - 150,
        "CERTIFICATE OF PARTICIPATION"
    )

    # Main text
    pdf.setFont("Helvetica", 14)
    pdf.drawCentredString(
        width / 2,
        height - 220,
        "This certificate is proudly presented to"
    )

    # Student name
    pdf.setFont("Helvetica-Bold", 22)
    pdf.drawCentredString(
        width / 2,
        height - 270,
        student_name
    )

    # Workshop details
    pdf.setFont("Helvetica", 14)
    pdf.drawCentredString(
        width / 2,
        height - 330,
        "for successfully participating in"
    )

    pdf.setFont("Helvetica-Bold", 18)
    pdf.drawCentredString(
        width / 2,
        height - 370,
        "AI Workshop"
    )

    pdf.setFont("Helvetica", 13)
    pdf.drawCentredString(
        width / 2,
        height - 420,
        "Date: 26 September 2026"
    )

    # Footer
    pdf.setFont("Helvetica", 11)
    pdf.drawCentredString(
        width / 2,
        100,
        "College Event Management System"
    )

    pdf.save()

    buffer.seek(0)

    # Safe filename
    safe_name = "".join(
        c for c in student_name
        if c.isalnum() or c in (" ", "_", "-")
    ).strip()

    filename = f"{safe_name}_Certificate.pdf"

    return send_file(
        buffer,
        as_attachment=True,
        download_name=filename,
        mimetype="application/pdf"
    )


# ---------------- START APPLICATION ----------------

if __name__ == "__main__":
    create_database()
    app.run(debug=True)