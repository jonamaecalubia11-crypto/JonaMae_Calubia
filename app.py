from flask import Flask, jsonify, request, render_template_string, redirect, url_for

app = Flask(__name__)

# ----------------------
# In-memory "database"
# ----------------------
students = [
    {"id": 1, "name": "Juan", "grade": 85, "section": "Zechariah"},
    {"id": 2, "name": "Maria", "grade": 90, "section": "Zechariah"},
    {"id": 3, "name": "Pedro", "grade": 70, "section": "Zion"}
]

PASS_MARK = 75

# ----------------------
# Shared CSS Template
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
    body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background-color: var(--light); margin: 0; padding: 20px; color: var(--dark); }
    .container { max-width: 900px; margin: auto; background: white; padding: 30px; border-radius: 12px; box-shadow: 0 4px 15px rgba(0,0,0,0.1); }
    h2 { color: var(--dark); border-bottom: 2px solid var(--primary); padding-bottom: 10px; margin-bottom: 20px; }
    
    /* Summary Cards */
    .summary-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 15px; margin-bottom: 30px; }
    .card { padding: 15px; border-radius: 8px; text-align: center; color: white; font-weight: bold; }
    .bg-avg { background: var(--primary); }
    .bg-pass { background: var(--success); }
    .bg-fail { background: var(--danger); }

    /* Table Styling */
    table { width: 100%; border-collapse: collapse; margin-top: 10px; }
    th { background-color: #f8f9fa; text-align: left; padding: 12px; border-bottom: 2px solid #dee2e6; }
    td { padding: 12px; border-bottom: 1px solid #eee; }
    tr:hover { background-color: #fcfcfc; }

    /* Buttons & Links */
    .btn { display: inline-block; padding: 8px 16px; border-radius: 5px; text-decoration: none; font-size: 14px; transition: 0.3s; border: none; cursor: pointer; }
    .btn-add { background: var(--primary); color: white; margin-bottom: 20px; }
    .btn-edit { color: var(--primary); font-weight: bold; }
    .btn-delete { color: var(--danger); font-weight: bold; }
    .btn:hover { opacity: 0.8; }

    /* Form Styling */
    input { width: 100%; padding: 10px; margin: 8px 0 20px; border: 1px solid #ccc; border-radius: 5px; box-sizing: border-box; }
    .badge { padding: 4px 8px; border-radius: 4px; font-size: 12px; color: white; }
    .pass { background: var(--success); }
    .fail { background: var(--danger); }
</style>
"""

# ----------------------
# Helper Functions
# ----------------------
def compute_summary():
    if not students: return {"average": 0, "passed": 0, "failed": 0}
    grades = [s["grade"] for s in students]
    passed = len([g for g in grades if g >= PASS_MARK])
    avg = round(sum(grades) / len(grades), 2)
    return {"average": avg, "passed": passed, "failed": len(grades) - passed}

def get_next_id():
    return max([s["id"] for s in students], default=0) + 1

# ----------------------
# Routes
# ----------------------
@app.route('/')
def home():
    return redirect(url_for('list_students'))

@app.route('/students')
def list_students():
    summary = compute_summary()
    html = BASE_CSS + """
    <div class="container">
        <h2>🎓 Student Management System</h2>
        
        <div class="summary-grid">
            <div class="card bg-avg">Avg Grade: {{summary.average}}</div>
            <div class="card bg-pass">Passed: {{summary.passed}}</div>
            <div class="card bg-fail">Failed: {{summary.failed}}</div>
        </div>

        <a href="/add_student_form" class="btn btn-add">+ Add New Student</a>

        <table>
            <tr>
                <th>ID</th>
                <th>Name</th>
                <th>Section</th>
                <th>Grade</th>
                <th>Status</th>
                <th>Actions</th>
            </tr>
            {% for s in students %}
            <tr>
                <td>{{s.id}}</td>
                <td><strong>{{s.name}}</strong></td>
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
                    <a href="/edit_student/{{s.id}}" class="btn-edit">Edit</a> | 
                    <a href="/delete_student/{{s.id}}" class="btn-delete" onclick="return confirm('Delete this record?')">Delete</a>
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
    <div class="container" style="max-width: 500px;">
        <h2>Add New Student</h2>
        <form action="/add_student" method="POST">
            <label>Full Name</label>
            <input type="text" name="name" placeholder="e.g. John Doe" required>
            <label>Grade (0-100)</label>
            <input type="number" name="grade" min="0" max="100" required>
            <label>Section</label>
            <input type="text" name="section" placeholder="e.g. Zion" required>
            <button type="submit" class="btn btn-add" style="width:100%">Save Student</button>
        </form>
        <center><a href="/students" style="color: #666; text-decoration: none;">← Back to List</a></center>
    </div>
    """
    return render_template_string(html)

@app.route('/add_student', methods=['POST'])
def add_student():
    try:
        name = request.form.get("name")
        grade = int(request.form.get("grade"))
        section = request.form.get("section")
        students.append({"id": get_next_id(), "name": name, "grade": grade, "section": section})
    except: pass
    return redirect(url_for('list_students'))

@app.route('/edit_student/<int:id>', methods=['GET', 'POST'])
def edit_student(id):
    student = next((s for s in students if s["id"] == id), None)
    if not student: return "Student not found", 404

    if request.method == 'POST':
        student["name"] = request.form["name"]
        student["grade"] = int(request.form["grade"])
        student["section"] = request.form["section"]
        return redirect(url_for('list_students'))

    html = BASE_CSS + """
    <div class="container" style="max-width: 500px;">
        <h2>Edit Student Details</h2>
        <form method="POST">
            <label>Name</label>
            <input type="text" name="name" value="{{student.name}}" required>
            <label>Grade</label>
            <input type="number" name="grade" min="0" max="100" value="{{student.grade}}" required>
            <label>Section</label>
            <input type="text" name="section" value="{{student.section}}" required>
            <button type="submit" class="btn btn-add" style="width:100%; background: var(--secondary)">Update Info</button>
        </form>
        <center><a href="/students" style="color: #666; text-decoration: none;">Cancel</a></center>
    </div>
    """
    return render_template_string(html, student=student)

@app.route('/delete_student/<int:id>')
def delete_student(id):
    global students
    students = [s for s in students if s["id"] != id]
    return redirect(url_for('list_students'))

if __name__ == '__main__':
    app.run(debug=True)
