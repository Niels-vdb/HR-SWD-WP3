from flask import render_template, request, jsonify, session, url_for, redirect
from sqlalchemy.sql import and_
from app import app, qrcode, db
from app.models import Class, Study, Meeting, Course
from app.api_routes import meetings_api
from flask_login import current_user, login_required
from app.alchemist import Alchemist as alchemist
from app.alchemist import SqliteQueries as query_model
from app.login_handler import get_user_role
from types import SimpleNamespace

import requests


@app.route('/student')
@app.route('/student/<meeting_id>')
@login_required
def student_screen(meeting_id=None):
    name = session["student_name"]
    name = name.split(' ')[0]

    if meeting_id == None:
        kwarq = {
        'name': name,
        'current_meeting_info': {}
        }
        return render_template('student-screen.html', kwarq=kwarq, title='Student Pagina')

    meeting_id = session['meeting_id']
    current_meeting = alchemist.get_meeting_by_id(meeting_id)
    course = alchemist.get_course_by_id(current_meeting.courseId)
    teacher = alchemist.get_teacher(current_meeting.teacher)
    current_meeting_info = {
        'teacher': teacher.name,
        'course': course.name,
        'current_meeting': current_meeting

    }
    kwarq = {
        'name': name,
        'current_meeting_info': current_meeting_info
    }
    return render_template('student-screen.html', kwarq=kwarq, title='Bijeenkomst Check In')


@ app.route('/present-screen')
@ login_required
def presentscreen():
    return render_template('presentscreen.html')


@ app.route('/docent-menu')
@ login_required
def teacher_menu():
    session["teacher_admin"]
    email = session["teacher_id"]
    results = alchemist.teacher_meeting_info(email)
    name = session["teacher_name"]
    name = name.split(' ')[0]
    return render_template('teacher-menu.html', results=results, name=name, title='Menu')


@ app.route('/beamer-scherm')
@ app.route('/beamer-scherm/<meeting_id>')
@ login_required
def beamer_screen(meeting_id=None):
    present = alchemist.present_in_meeting(meeting_id)
    pres_students = []
    for st in present:
        student = alchemist.get_student_by_id(st.studentId)
        pres_students.append(student)

    absent = alchemist.absent_in_meeting(meeting_id)
    abs_students = []
    for st in absent:
        student = alchemist.get_student_by_id(st.studentId)
        abs_students.append(student)

    called_off = alchemist.called_off_meeting(meeting_id)
    cal_off_students = []
    for st in called_off:
        student = alchemist.get_student_by_id(st.studentId)
        cal_off_students.append(student)

    # qr = qrcode(f'http://192.168.2.8:81/student/{meeting_id}')
    qr = qrcode(f'http://192.168.180.160:80/student/{meeting_id}')

    kwarq = {
        'students_present': pres_students,
        'students_absent': abs_students,
        'students_called_off': cal_off_students,
        'meeting_id': meeting_id,
        'qr': qr
    }

    return render_template('beamer-screen.html', kwarq=kwarq, title='Bijeenkomst')


@app.route('/manage_account', methods=['GET'])
@login_required
def manage_account():
    try:
        if current_user.isAdmin:
            role = get_user_role(current_user)
            return render_template("manage_account.html", role=role, studies=Study.query.all())
    except:
        return redirect(url_for('teacher_menu'))

    return redirect(url_for('teacher_menu'))

@ app.route('/bijeenkomst-aanmaken', methods={"GET", "POST"})
@ login_required
def make_meeting_screen():
    studies = alchemist.get_studies()
    courses = alchemist.get_courses()

    class_in_study_dict = {}

    for study in studies:
        c = db.session.query(Class).filter(
            Class.studyId == study.studyId).all()
        if study.studyId in class_in_study_dict:
            class_in_study_dict[study.studyId].append(c)
        else:
            class_in_study_dict[study.studyId] = c

    kwarq = {
        'studies': class_in_study_dict.items(),
        'courses': courses
    }

    return render_template('create-meeting.html', kwarq=kwarq, title='Bijeenkomst Aanmaken')


@ app.route('/playground')
def playground():
    return render_template('playground.html')


@app.route("/get-student-presence-course", methods=["GET"])
def get_student_presence_course():
    student_id = request.args.get("student_id", default=1, type=int)
    course_name = request.args.get("course_name", default="Nederlands", type=str)
    name = query_model.get_name_for_student_id(student_id)
    presence_count = query_model.get_course_presence(student_id, course_name)
    absence_count = query_model.get_course_absence(student_id, course_name)
    checked_out_count = query_model.get_course_checked_out(student_id, course_name)
    # no_of_meetings = query_model.count_no_of_meetings_for_student_id(student_id)
    total = float(60)
    presence_percentage = presence_count / total * 100 if total > 0 else 0
    absence_percentage = absence_count / total * 100 if total > 0 else 0
    checked_out_percentage = checked_out_count / total * 100 if total > 0 else 0
    student = {
        "presence_count": presence_count,
        "absence_count": absence_count,
        "checked_out_count": checked_out_count,
        "absence_percentage": round(absence_percentage),
        "presence_percentage": round(presence_percentage),
        "checked_out_percentage": round(checked_out_percentage),
        "student_id": student_id,
        "name": name
    }
    return jsonify(student)



@app.route("/get-student-presence", methods=["GET"])
def get_student_presence():
    student_id = request.args.get("student_id", default=1, type=int)
    name = query_model.get_name_for_student_id(student_id)
    presence_count = query_model.count_meeting_presence(student_id)
    absence_count = query_model.count_meeting_absence(student_id)
    checked_out_count = query_model.count_meeting_checked_out(student_id)
    no_of_meetings = query_model.count_no_of_meetings_for_student_id(student_id)
    total = float(no_of_meetings)
    presence_percentage = presence_count / total * 100 if total > 0 else 0
    absence_percentage = absence_count / total * 100 if total > 0 else 0
    checked_out_percentage = checked_out_count / total * 100 if total > 0 else 0
    student = {
        "presence_count": presence_count,
        "absence_count": absence_count,
        "checked_out_count": checked_out_count,
        "absence_percentage": round(absence_percentage),
        "presence_percentage": round(presence_percentage),
        "checked_out_percentage": round(checked_out_percentage),
        "student_id": student_id,
        "name": name
    }
    return jsonify(student)



@app.route('/student-lookup', methods=['GET', 'POST'])
def student_search():
    all_students = [SimpleNamespace(student_id=student_id, name=name) for student_id, name in
                    query_model.get_students()]
    course_names = ["Algemeen", *[course.name for course in alchemist.get_courses()]]

    return render_template('lookupscreen.html', students=all_students, courses=course_names)


@ app.route('/apitest')
def apitest():
    return render_template('ftesttemplate.html')


@app.route('/create-account', methods=['GET', 'POST'])
@login_required
def create_account():
    if request.method == "POST":
        print("Method was POST")

    role = get_user_role(current_user)
    return render_template("create-account.html", role=role)




@app.route('/teacher_meeting_history')
@app.route('/teacher_meeting_history/<meeting_id>', methods=['GET'])
@login_required
def teacher_meeting_history(meeting_id=None):
    all_meetings = Meeting.query.filter((Meeting.teacher==current_user.email) & (Meeting.finished == 1)).all()

    if meeting_id:
        meeting_info = meetings_api(meeting_id).get_json()
        return render_template("teacher_meeting_history.html", meetings=None, meeting_info=meeting_info)

    return render_template("teacher_meeting_history.html", meetings=all_meetings, meeting_info=None)