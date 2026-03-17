from flask import Flask, request, redirect, url_for, render_template_string
import sqlite3

app = Flask(__name__)

import os
DB_NAME = os.path.join(os.getcwd(), "students.db")
PASS_MARK = 75

# ----------------------
# CSS
# ----------------------
BASE_CSS = """
<style>
:root {
    --primary: #4a90e2;
    --secondary: #f39c12;
    --danger: #e74c3c;
    --success: #2ecc71;
    --dark: #2c3e50;
    --light: #f4f7f6;
}
body {
    font-family: 'Segoe UI', sans-serif;
    background-color: var(--light);
    margin:0; padding:20px;
}
.container {
    max-width:900px;
    margin:auto;
    background:white;
    padding:30px;
    border-radius:12px;
    box-shadow:0 4px 15px rgba(0,0,0,0.1);
}
.summary-grid {
    display:grid;
    grid-template-columns:repeat(3,1fr);
    gap:15px;
    margin-bottom:30px;
}
.card {
    padding:15px;
    border-radius:8px;
    text-align:center;
    color:white;
    font-weight:bold;
}
.bg-avg { background: var(--primary); }
.bg-pass { background: var(--success); }
.bg-fail { background: var(--danger); }

table {
    width:100%;
    border-collapse:collapse;
}
th, td {
    padding:12px;
    border-bottom:1px solid #eee;
}
.badge { padding:4px 8px; border-radius:4px; color:white; }
.pass { background: var(--success); }
.fail { background: var(--danger); }

.btn { padding:8px 16px; border:none; cursor:pointer; }
.btn-add { background: var(--primary); color:white; }
</style>
"""

# ----------------------
# DATABASE
# ----------------------
def get_db_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            grade INTEGER,
            section TEXT
        )
    """)
    conn.commit()
    conn.close()

def compute_summary():
    conn = get_db_connection()
    grades = [row["grade"] for row in conn.execute("SELECT grade FROM students").fetchall()]
    conn.close()

    if not grades:
        return {"average": 0, "passed": 0, "failed": 0}

    avg = round(sum(grades) / len(grades), 2)
    passed = len([g for g in grades if g >= PASS_MARK])

    return {"average": avg, "passed": passed, "failed": len(grades) - passed}

# ----------------------
# ROUTES
# ----------------------
@app.route('/students')
def list_students():
    conn = get_db_connection()
    students = conn.execute("SELECT * FROM students").fetchall()
    conn.close()

    summary = compute_summary()

    html = BASE_CSS + """
    <div class="container">
        <h2>🎓 Student Management System</h2>

        <div class="summary-grid">
            <div class="card bg-avg">Avg: {{summary.average}}</div>
            <div class="card bg-pass">Passed: {{summary.passed}}</div>
            <div class="card bg-fail">Failed: {{summary.failed}}</div>
        </div>

        <a href="/add_student_form" class="btn btn-add">+ Add Student</a>

        <table>
        <tr><th>ID</th><th>Name</th><th>Section</th><th>Grade</th><th>Status</th><th>Actions</th></tr>
        {% for s in students %}
        <tr>
            <td>{{s.id}}</td>
            <td>{{s.name}}</td>
            <td>{{s.section}}</td>
            <td>{{s.grade}}</td>
            <td>
                {% if s.grade >= 75 %}
                <span class="badge pass">PASSED</span>
                {% else %}
                <span class="badge fail">FAILED</span>
                {% endif %}
            </td>
            <td>
                <a href="/edit_student/{{s.id}}">Edit</a> |
                <a href="/delete_student/{{s.id}}">Delete</a>
            </td>
        </tr>
        {% endfor %}
        </table>
    </div>
    """
    return render_template_string(html, students=students, summary=summary)

@app.route('/add_student_form')
def add_student_form():
    html = BASE_CSS + """
    <div class="container">
        <h2>Add Student</h2>
        <form method="POST" action="/add_student">
            <input type="text" name="name" placeholder="Name" required>
            <input type="number" name="grade" placeholder="Grade" required>
            <input type="text" name="section" placeholder="Section" required>
            <button class="btn btn-add">Save</button>
        </form>
    </div>
    """
    return render_template_string(html)

@app.route('/add_student', methods=['POST'])
def add_student():
    name = request.form.get("name")
    grade = int(request.form.get("grade") or 0)
    section = request.form.get("section")

    conn = get_db_connection()
    conn.execute("INSERT INTO students (name, grade, section) VALUES (?, ?, ?)",
                 (name, grade, section))
    conn.commit()
    conn.close()

    return redirect(url_for('list_students'))

@app.route('/edit_student/<int:id>', methods=['GET','POST'])
def edit_student(id):
    conn = get_db_connection()
    student = conn.execute("SELECT * FROM students WHERE id=?", (id,)).fetchone()

    if not student:
        conn.close()
        return "Not found", 404

    if request.method == 'POST':
        name = request.form.get("name")
        grade = int(request.form.get("grade") or 0)
        section = request.form.get("section")

        conn.execute("UPDATE students SET name=?, grade=?, section=? WHERE id=?",
                     (name, grade, section, id))
        conn.commit()
        conn.close()
        return redirect(url_for('list_students'))

    conn.close()

    html = BASE_CSS + """
    <div class="container">
        <h2>Edit Student</h2>
        <form method="POST">
            <input type="text" name="name" value="{{student.name}}" required>
            <input type="number" name="grade" value="{{student.grade}}" required>
            <input type="text" name="section" value="{{student.section}}" required>
            <button class="btn btn-add">Update</button>
        </form>
    </div>
    """
    return render_template_string(html, student=student)

@app.route('/delete_student/<int:id>')
def delete_student(id):
    conn = get_db_connection()
    conn.execute("DELETE FROM students WHERE id=?", (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('list_students'))

# ----------------------
# RUN
# ----------------------
init_db()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
