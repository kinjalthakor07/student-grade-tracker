from flask import Flask, render_template, request, session
import numpy as np
import matplotlib.pyplot as plt
import os

app = Flask(__name__)
app.secret_key = "secret"

os.makedirs("static", exist_ok=True)


def create_chart(students):

    names = [s["name"] for s in students]
    averages = [s["avg"] for s in students]

    plt.figure(figsize=(6,4))
    plt.bar(names, averages)
    plt.title("Class Performance (Average Marks)")
    plt.ylabel("Average")

    path = "static/chart.png"
    plt.savefig(path)
    plt.close()

    return path


@app.route("/", methods=["GET", "POST"])
def home():

    if "students" not in session:
        session["students"] = []

    students = session["students"]

    if request.method == "POST":

        name = request.form["name"]
        math = int(request.form["math"])
        science = int(request.form["science"])
        english = int(request.form["english"])

        marks = np.array([math, science, english])

        total = int(np.sum(marks))
        avg = float(np.mean(marks))

        status = "Pass" if avg >= 50 else "Fail"

        student = {
            "name": name,
            "math": math,
            "science": science,
            "english": english,
            "total": total,
            "avg": round(avg,2),
            "status": status
        }

        students.append(student)
        session["students"] = students


    chart = None
    topper = None
    class_avg = 0
    pass_count = 0
    fail_count = 0

    if len(students) > 0:

        class_avg = round(np.mean([s["avg"] for s in students]),2)

        topper = max(students, key=lambda x: x["total"])["name"]

        pass_count = len([s for s in students if s["status"] == "Pass"])
        fail_count = len([s for s in students if s["status"] == "Fail"])

        chart = create_chart(students)

    return render_template(
        "index.html",
        students=students,
        class_avg=class_avg,
        topper=topper,
        pass_count=pass_count,
        fail_count=fail_count,
        chart=chart
    )


if __name__ == "__main__":
    app.run(debug=True)