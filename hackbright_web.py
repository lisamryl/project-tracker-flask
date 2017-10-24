"""A web application for tracking projects, students, and student grades."""

from flask import Flask, request, render_template

import hackbright

app = Flask(__name__)


@app.route("/student")
def get_student():
    """Show information about a student."""

    github = request.args.get('github')

    first, last, github = hackbright.get_student_by_github(github)
    grades = hackbright.get_grades_by_github(github)

    return render_template("student_info.html",
                           first=first,
                           last=last,
                           github=github,
                           grades=grades)


@app.route("/student-search")
def get_student_form():
    """Show form for searching for a student."""

    return render_template("student_search.html")


@app.route("/student-add")
def student_add():
    """Add a student."""

    return render_template("student_add.html")


@app.route("/student-added", methods=['POST'])
def student_added():
    """Pushes to database and returns acknowledgement to student."""

    github = request.form.get("github")
    fname = request.form.get("fname")
    lname = request.form.get("lname")

    hackbright.make_new_student(fname, lname, github)

    return render_template("student_added.html",
                           fname=fname,
                           lname=lname,
                           github=github)

@app.route("/projects")
def display_projects():
    """Display list of projects and their details. """

    projects = hackbright.get_projects()

    project_grades = {}

    for project in projects:
        grades = hackbright.get_grades_by_title(project[0])
        project_grades[project[0]] = grades

    return render_template("projects.html", projects=projects, project_grades=project_grades)

if __name__ == "__main__":
    hackbright.connect_to_db(app)
    app.run(debug=True)
