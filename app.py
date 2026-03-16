from flask import Flask, jsonify, request, render_template_string

app = Flask(__name__)

# Home
@app.route('/')
def home():
    return "Welcome to my first API!"

# Student table view
@app.route('/student')
def get_student():

    grade = int(request.args.get('grade', 0))

    name = "Juan"
    section = "Zechariah"

    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Student Info</title>
        <style>
            body {{
                font-family: Arial;
                background:#f4f6f9;
                text-align:center;
            }}

            h2 {{
                color:#333;
            }}

            table {{
                margin:auto;
                border-collapse: collapse;
                width: 50%;
                background:white;
                box-shadow:0px 0px 10px rgba(0,0,0,0.1);
            }}

            th {{
                background:#3498db;
                color:white;
                padding:10px;
            }}

            td {{
                padding:10px;
                border:1px solid #ddd;
            }}

            tr:hover {{
                background:#f1f1f1;
            }}
        </style>
    </head>
    <body>

    <h2>Student Information</h2>

    <table>
        <tr>
            <th>Name</th>
            <th>Section</th>
            <th>Grade</th>
        </tr>

        <tr>
            <td>{name}</td>
            <td>{section}</td>
            <td>{grade}</td>
        </tr>

    </table>

    </body>
    </html>
    """

    return render_template_string(html)


# JSON version
@app.route('/student-json')
def student_json():
    grade = int(request.args.get('grade', 0))

    return jsonify({
        "grade": grade,
        "name": "Juan",
        "section": "Zechariah"
    })


if __name__ == '__main__':
    app.run(debug=True)
