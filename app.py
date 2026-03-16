from flask import Flask, jsonify, request

app = Flask(__name__)

@app.route('/')
def home():
    return "Welcome to my first API!"

# Updated student route with pass/fail logic
@app.route('/student')
def get_student():
    # Get grade from query parameter (default = 0)
    grade = int(request.args.get('grade', 0))

    # Determine pass or fail
    remarks = "Pass" if grade >= 75 else "Fail"

    return jsonify({
        "name": "Juan",
        "grade": grade,
        "section": "Zechariah",
        "remarks": remarks
    })

@app.route('/hello')
def say_hello():
    name = request.args.get('name', 'Student')
    return jsonify({
        "message": f"Hello, {name}!"
    })

if __name__ == '__main__':
    app.run(debug=True)