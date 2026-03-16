from flask import Flask, jsonify, request, render_template_string, redirect, url_for

app = Flask(__name__)

# In-memory database
students = [
    {"id": 1, "name": "Juan", "grade": 85, "section": "Zechariah"},
    {"id": 2, "name": "Maria", "grade": 90, "section": "Zechariah"},
    {"id": 3, "name": "Pedro", "grade": 70, "section": "Zion"}
]

# Home
@app.route('/')
def home():
    return redirect(url_for('list_students'))


# View all students
@app.route('/students')
def list_students():

    html = """
    <h2>Student List</h2>

    <a href="/add_student_form">Add New Student</a>

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

    return render_template_string(html, students=students)


# Add Student Form
@app.route('/add_student_form')
def add_student_form():

    html = """
    <h2>Add New Student</h2>

    <form action="/add_student" method="POST">
        Name:<br>
        <input type="text" name="name"><br><br>

        Grade:<br>
        <input type="number" name="grade"><br><br>

        Section:<br>
        <input type="text" name="section"><br><br>

        <button type="submit">Add Student</button>
    </form>

    <br>
    <a href="/students">Back to List</a>
    """

    return render_template_string(html)


# Add Student
@app.route('/add_student', methods=['POST'])
def add_student():

    name = request.form.get("name")
    grade = int(request.form.get("grade"))
    section = request.form.get("section")

    new_id = len(students) + 1

    new_student = {
        "id": new_id,
        "name": name,
        "grade": grade,
        "section": section
    }

    students.append(new_student)

    return redirect(url_for('list_students'))


# Edit Student
@app.route('/edit_student/<int:id>', methods=['GET', 'POST'])
def edit_student(id):

    student = next((s for s in students if s["id"] == id), None)

    if not student:
        return "Student not found", 404

    if request.method == 'POST':

        student["name"] = request.form["name"]
        student["grade"] = int(request.form["grade"])
        student["section"] = request.form["section"]

        return redirect(url_for('list_students'))

    html = """
    <h2>Edit Student</h2>

    <form method="POST">

        Name:<br>
        <input type="text" name="name" value="{{student.name}}"><br><br>

        Grade:<br>
        <input type="number" name="grade" value="{{student.grade}}"><br><br>

        Section:<br>
        <input type="text" name="section" value="{{student.section}}"><br><br>

        <button type="submit">Update</button>

    </form>

    <br>
    <a href="/students">Back</a>
    """

    return render_template_string(html, student=student)


# Delete Student
@app.route('/delete_student/<int:id>')
def delete_student(id):

    global students

    students = [s for s in students if s["id"] != id]

    return redirect(url_for('list_students'))


# API JSON view
@app.route('/api/students')
def api_students():
    return jsonify(students)


if __name__ == '__main__':
    app.run(debug=True)
