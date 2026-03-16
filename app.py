from flask import Flask, jsonify, request

app = Flask(__name__)

# Home route
@app.route('/')
def home():
    return jsonify({
        "message": "Welcome to my first API!",
        "author": "Jona Mae Calubia",
        "available_routes": [
            "/student?grade=90",
            "/hello?name=Jona",
            "/api-info"
        ]
    })


# API information route
@app.route('/api-info')
def api_info():
    return jsonify({
        "api_name": "Student Grade API",
        "version": "1.0",
        "description": "A simple API that checks student grade and greeting message."
    })


# Updated student route with pass/fail logic
@app.route('/student')
def get_student():
    grade = request.args.get('grade')

    # Check if grade is provided
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
