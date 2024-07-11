from flask import Flask, request, redirect
from flask import render_template
from flask import current_app as app
from .models import Student, Course
from .database import db

@app.route("/", methods=['GET', 'POST'])
def index():
	all_students = Student.query.all()
	return render_template("index.html", students=all_students)


@app.route("/student/create", methods=['GET', 'POST'])
def create_student():
	if request.method == 'GET':
		courses = Course.query.all()
		return render_template("create_student.html", courses=courses)

	if request.method == 'POST':
		roll_number = request.form.get('roll')
		first_name = request.form.get('f_name')
		last_name = request.form.get('l_name')
		courses = request.form.getlist('courses')

		student = Student(roll_number=roll_number, first_name=first_name, last_name=last_name)
		for id in courses:
			course = Course.query.filter(Course.course_id == id).one()
			student.courses.append(course)
		try:
			db.session.add(student)
			db.session.commit()
		except:
			return render_template("already_exists.html")
		return redirect("/")

@app.route("/student/<int:student_id>/update", methods=['GET', 'POST'])
def update_student(student_id):
	student = Student.query.filter(Student.student_id == student_id).one()
	if request.method == 'GET':
		courses = Course.query.all()
		return render_template("update_student.html", student=student, courses=courses)

	if request.method == 'POST':
		first_name = request.form.get('f_name')
		last_name = request.form.get('l_name')
		courses = request.form.getlist('courses')
		student.courses = []
		student.first_name = first_name
		student.last_name = last_name

		for id in courses:
			course = Course.query.filter(Course.course_id == id).one()
			student.courses.append(course)

		db.session.commit()

		return redirect("/")

@app.route("/student/<int:student_id>/delete")
def delete_student(student_id):
	student = Student.query.filter(Student.student_id == student_id).one()
	db.session.delete(student)
	db.session.commit()
	return redirect("/")

@app.route("/student/<int:student_id>")
def student_details(student_id):
	student = Student.query.filter(Student.student_id == student_id).one()
	courses = []
	for course in student.courses:
		courses.append(course)

	return render_template("student_details.html", student=student, courses=courses)
