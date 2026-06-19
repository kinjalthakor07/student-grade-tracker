from flask import Flask, render_template, request
import numpy as np
import matplotlib.pyplot as plt

app = Flask(__name__)

students = []


def create_chart(students):
    names = [s["name"] for s in students]
    averages = [s["avg"] for s in students]

    plt.figure(figsize=(8, 4))
    plt.bar(names, averages)

    plt.title("Student Average Marks")
    plt.ylabel("Average Marks")
    plt.tight_layout()

    plt.savefig("static/chart.png")
    plt.close()


@app.route("/", methods=["GET", "POST"])
def home():

    if request.method == "POST":

        try:
            name = request.form["name"].strip()

            math = int(request.form["math"])
            science = int(request.form["science"])
            english = int(request.form["english"])

            # Validation
            if not (
                0 <= math <= 100 and
                0 <= science <= 100 and
                0 <= english <= 100
            ):
                return "Marks must be between 0 and 100"

            marks = np.array([math, science, english])

            total = int(np.sum(marks))
            avg = round(float(np.mean(marks)), 2)

            status = "Pass" if avg >= 50 else "Fail"

            students.append({
                "name": name,
                "math": math,
                "science": science,
                "english": english,
                "total": total,
                "avg": avg,
                "status": status
            })

        except ValueError:
            return "Please enter valid numbers"

    class_avg = 0
    topper = "-"
    pass_count = 0
    fail_count = 0

    if students:

        class_avg = round(
            np.mean([s["avg"] for s in students]),
            2
        )

        topper = max(
            students,
            key=lambda x: x["total"]
        )["name"]

        pass_count = sum(
            1 for s in students
            if s["status"] == "Pass"
        )

        fail_count = sum(
            1 for s in students
            if s["status"] == "Fail"
        )

        create_chart(students)

    return render_template(
        "index.html",
        students=students,
        class_avg=class_avg,
        topper=topper,
        pass_count=pass_count,
        fail_count=fail_count
    )


if __name__ == "__main__":
    app.run(debug=False)