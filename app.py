from flask import Flask, jsonify, request, render_template_string

app = Flask(__name__)

# Home route with HTML design
@app.route('/')
def home():
    html = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Student Grade API</title>
        <style>
            body{
                font-family: Arial;
                background:#f4f6f9;
                text-align:center;
            }
            h1{
                color:#2c3e50;
            }
            table{
                margin:auto;
                border-collapse:collapse;
                width:60%;
                background:white;
                box-shadow:0 0 10px rgba(0,0,0,0.1);
            }
            th,td{
                padding:12px;
                border:1px solid #ddd;
            }
            th{
                background:#3498db;
                color:white;
            }
            tr:hover{
                background:#f1f1f1;
            }
            a{
                text-decoration:none;
                color:#3498db;
                font-weight:bold;
            }
        </style>
    </head>
    <body>

    <h1>Student Grade API</h1>
    <p>Author: Jona Mae Calubia</p>

    <table>
        <tr>
            <th>API Endpoint</th>
            <th>Description</th>
            <th>Example</th>
        </tr>

        <tr>
            <td>/student</td>
            <td>Check if student passed or failed</td>
            <td><a href="/student?grade=90">Try Example</a></td>
        </tr>

        <tr>
            <td>/hello</td>
            <td>Greeting API</td>
            <td><a href="/hello?name=Jona">Try Example</a></td>
        </tr>

        <tr>
            <td>/api-info</td>
            <td>API information</td>
            <td><a href="/api-info">View Info</a></td>
        </tr>

    </table>

    </body>
    </html>
    """
    return render_template_string(html)


# API information route
@app.route('/api-info')
def api_info():
    return jsonify({
        "api_name": "Student Grade API",
        "version": "1.0",
        "description": "A simple API that checks student grade and greeting message."
    })


# Student route
@app.route('/student')
def get_student():
    grade = request.args.get('grade')

    if grade is None:
        return jsonify({
            "error": "Please provide a grade using ?grade=value"
        }), 400

    try:
        grade = int(grade)
    except ValueError:
        return jsonify({
            "error": "Grade must be a number"
        }), 400

    remarks = "Pass" if grade >= 75 else "Fail"

    return jsonify({
        "name": "Juan",
        "section": "Zechariah",
        "grade": grade,
        "remarks": remarks
    })


# Hello route
@app.route('/hello')
def say_hello():
    name = request.args.get('name', 'Student')

    return jsonify({
        "message": f"Hello, {name}! Welcome to my API."
    })


if __name__ == '__main__':
    app.run(debug=True)
