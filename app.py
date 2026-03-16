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

PASS_MARK = 75  # Define passing grade globally


# ----------------------
# Helper Functions
# ----------------------
def compute_summary():
    """Compute average, passed, and failed counts"""
    if not students:
        return {"average": 0, "passed": 0, "failed": 0}
    
    grades = [s["grade"] for s in students]
    passed = len([g for g in grades if g >= PASS_MARK])
    failed = len(grades) - passed
    avg = round(sum(grades) / len(grades), 2)
    
    return {"average": avg, "passed": passed, "failed": failed}


def get_next_id():
    """Get the next available student ID"""
    if not students:
        return 1
    return max(s["id"] for s in students) + 1


# ----------------------
# Routes
# ----------------------
@app.route('/')
def home():
    return redirect(url_for('list_students'))


@app.route('/students')
def list_students():
    summary = compute_summary()
    html = """
    <h2>Student List</h2>
    <a href="/add_student_form">Add New Student</a><br><br>

    <strong>Summary:</strong>
    <ul>
        <li>Average Grade: {{summary.average}}</li>
        <li>Passed: {{summary.passed}}</li>
        <li>Failed: {{summary.failed}}</li>
    </ul>

    <table border="1" cellpadding="10">
        <tr>
            <th>ID</th>
            <th>Name</th>
            <th>Grade</th>
            <th>Section</th>
            <th>Actions</th>
        </tr>
        {% for s in students %}
        <tr>
            <td>{{s.id}}</td>
            <td>{{s.name}}</td>
            <td>{{s.grade}}</td>
            <td>{{s.section}}</td>
            <td>
                <a href="/edit_student/{{s.id}}">Edit</a> |
                <a href="/delete_student/{{s.id}}">Delete</a>
            </td>
        </tr>
        {% endfor %}
    </table>
    """
    return render_template_string(html, students=students, summary=summary)


@app.route('/add_student_form')
def add_student_form():
    html = """
    <h2>Add New Student</h2>
    <form action="/add_student" method="POST">
        Name:<br><input type="text" name="name" required><br><br>
        Grade:<br><input type="number" name="grade" min="0" max="100" required><br><br>
        Section:<br><input type="text" name="section" required><br><br>
        <button type="submit">Add Student</button>
    </form>
    <br><a href="/students">Back to List</a>
    """
    return render_template_string(html)


@app.route('/add_student', methods=['POST'])
def add_student():
    try:
        name = request.form.get("name")
        grade = int(request.form.get("grade"))
        section = request.form.get("section")
    except (TypeError, ValueError):
        return "Invalid input. Please provide name, grade (0-100), and section.", 400

    new_student = {"id": get_next_id(), "name": name, "grade": grade, "section": section}
    students.append(new_student)
    return redirect(url_for('list_students'))


@app.route('/edit_student/<int:id>', methods=['GET', 'POST'])
def edit_student(id):
    student = next((s for s in students if s["id"] == id), None)
    if not student:
        return "Student not found", 404

    if request.method == 'POST':
        try:
            student["name"] = request.form["name"]
            student["grade"] = int(request.form["grade"])
            student["section"] = request.form["section"]
        except (TypeError, ValueError):
            return "Invalid input.", 400
        return redirect(url_for('list_students'))

    html = """
    <h2>Edit Student</h2>
    <form method="POST">
        Name:<br><input type="text" name="name" value="{{student.name}}" required><br><br>
        Grade:<br><input type="number" name="grade" min="0" max="100" value="{{student.grade}}" required><br><br>
        Section:<br><input type="text" name="section" value="{{student.section}}" required><br><br>
        <button type="submit">Update</button>
    </form>
    <br><a href="/students">Back</a>
    """
    return render_template_string(html, student=student)


@app.route('/delete_student/<int:id>')
def delete_student(id):
    global students
    students = [s for s in students if s["id"] != id]
    return redirect(url_for('list_students'))


# ----------------------
# API Endpoints
# ----------------------
@app.route('/api/students')
def api_students():
    return jsonify(students)


@app.route('/api/summary')
def api_summary():
    return jsonify(compute_summary())


# ----------------------
# Run Flask
# ----------------------
if __name__ == '__main__':
    app.run(debug=True)
