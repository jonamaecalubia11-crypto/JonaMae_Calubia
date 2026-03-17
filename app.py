from flask import Flask, request, redirect, url_for, render_template_string
import sqlite3
import os

app = Flask(__name__)

DB_NAME = os.path.join(os.getcwd(), "students.db")
PASS_MARK = 75

# ----------------------
# MODERN CSS
# ----------------------
BASE_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600&display=swap');

:root {
    --primary: #6c63ff;
    --secondary: #00b894;
    --danger: #ff4757;
    --success: #2ed573;
    --dark: #2f3542;
    --light: #f1f2f6;
}

* {
    box-sizing: border-box;
}

body {
    font-family: 'Poppins', sans-serif;
    background: linear-gradient(135deg, #667eea, #764ba2);
    margin: 0;
    padding: 20px;
}

.container {
    max-width: 1000px;
    margin: auto;
    background: #fff;
    padding: 30px;
    border-radius: 16px;
    box-shadow: 0 10px 30px rgba(0,0,0,0.15);
    animation: fadeIn 0.5s ease;
}

h2 {
    margin-bottom: 20px;
}

.summary-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
    gap: 15px;
    margin-bottom: 25px;
}

.card {
    padding: 20px;
    border-radius: 12px;
    text-align: center;
    color: white;
    font-weight: 500;
    transition: 0.3s;
}

.card:hover {
    transform: translateY(-5px);
}

.bg-avg { background: linear-gradient(135deg, #6c63ff, #4834d4); }
.bg-pass { background: linear-gradient(135deg, #2ed573, #1eae60); }
.bg-fail { background: linear-gradient(135deg, #ff4757, #c0392b); }

.btn {
    padding: 10px 18px;
    border-radius: 8px;
    text-decoration: none;
    font-size: 14px;
    transition: 0.3s;
}

.btn-add {
    background: var(--primary);
    color: white;
    display: inline-block;
    margin-bottom: 15px;
}

.btn-add:hover {
    background: #574bdb;
}

table {
    width: 100%;
    border-collapse: collapse;
    border-radius: 12px;
    overflow: hidden;
}

thead {
    background: var(--primary);
    color: white;
}

th, td {
    padding: 14px;
    text-align: center;
}

tbody tr:nth-child(even) {
    background: #f9f9f9;
}

tbody tr:hover {
    background: #f1f2f6;
}

.badge {
    padding: 5px 10px;
    border-radius: 20px;
    font-size: 12px;
}

.pass {
    background: var(--success);
    color: white;
}

.fail {
    background: var(--danger);
    color: white;
}

a {
    text-decoration: none;
    color: var(--primary);
    font-weight: 500;
}

a:hover {
    text-decoration: underline;
}

form {
    display: grid;
    gap: 15px;
}

input {
    padding: 12px;
    border-radius: 8px;
    border: 1px solid #ddd;
}

input:focus {
    outline: none;
    border-color: var(--primary);
}

button {
    padding: 10px;
    border: none;
    border-radius: 8px;
    background: var(--primary);
    color: white;
    cursor: pointer;
}

button:hover {
    background: #574bdb;
}

@keyframes fadeIn {
    from { opacity: 0; transform: translateY(10px);}
    to { opacity: 1; transform: translateY(0);}
}
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
@app.route('/')
def home():
    return redirect(url_for('list_students'))

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
            <div class="card bg-avg">Average<br><strong>{{summary.average}}</strong></div>
            <div class="card bg-pass">Passed<br><strong>{{summary.passed}}</strong></div>
            <div class="card bg-fail">Failed<br><strong>{{summary.failed}}</strong></div>
        </div>

        <a href="/add_student_form" class="btn btn-add">+ Add Student</a>

        <table>
            <thead>
                <tr>
                    <th>ID</th><th>Name</th><th>Section</th>
                    <th>Grade</th><th>Status</th><th>Actions</th>
                </tr>
            </thead>
            <tbody>
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
            </tbody>
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
            <button>Save</button>
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
            <button>Update</button>
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
