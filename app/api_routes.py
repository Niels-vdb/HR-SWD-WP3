from app import app, db, bcrypt
from flask import request, jsonify, session, redirect, url_for, Response
from flask_login import login_required

from app.models import *
from app.alchemist import Alchemist as alchemist
from app.alchemist import SqliteQueries as query_model
from app.login_handler import get_user_role

from datetime import datetime


@app.route('/get_user_by_pk')
@login_required
def get_user_by_pk():
    student = Student.query.filter_by(
        studentId=f'{request.args.get("id")}').first()
    studies = []
    meetings = []

    for study in student.studies:
        stud = db.session.query(Class).join(Study).filter(
            Study.studyId == study.studyId).first()
        stud = db.session.query(Class).join(Study).filter(
            Study.studyId == study.studyId).first()
        studies.append({
            'study': stud.studyId,
            'class': study.name
        })
    for meeting in student.meetings:
        teacher = db.session.query(Teacher).filter(
            Teacher.email == f'{meeting.teacher}').first()
        course = db.session.query(Course).filter(
            Course.courseId == f'{meeting.courseId}').first()
        teacher = db.session.query(Teacher).filter(
            Teacher.email == f'{meeting.teacher}').first()
        course = db.session.query(Course).filter(
            Course.courseId == f'{meeting.courseId}').first()
        meetings.append({
            # 'Date': course.dateAndTime,
            'teacher': teacher.name,
            'course': course.name
        })

    return jsonify(studentId=student.studentId, name=student.name, studies=studies, meetings=meetings)


@app.route('/get_all_classes_of_study')
# @login_required
def get_all_classes_of_study():
    classes = []
    for classroom in Class.query.filter_by(studyId=f'{request.args.get("studyId")}').all():
        a_classroom = {
            "classId": classroom.classId,
            "name": classroom.name,
        }
        classes.append(a_classroom)

    return jsonify(classes)


@app.route('/get_all_students_of_class')
# @login_required
def get_all_students_of_class():
    class_id = request.args.get('classId')
    students = []
    all_students = db.session.query(class_to_student_table).filter(
        class_to_student_table.c.classId == class_id).all()

    for student in all_students:
        student_object = Student.query.filter_by(
            studentId=student.studentId).one()

        a_student = {
            "studentId": student_object.studentId,
            "name": student_object.name
        }
        students.append(a_student)

    return jsonify(students)


@app.route('/classes', methods=["GET", "POST"])
@app.route('/classes/<class_id>', methods=["GET", "DELETE"])
def classes_api(class_id=None):
    if request.method == "GET":
        if class_id == None:
            classes = alchemist.get_all_classes()
            class_info = []
            for c, study in classes:
                class_info.append({
                    'class_id': c.classId,
                    'class_name': c.name,
                    'study': study.name
                })
            return class_info
        else:
            clas = alchemist.get_class(class_id)
            students = alchemist.get_students_in_class(class_id)
            student_list = []

            for student in students.students:
                student_list.append({
                    'name': student.name,
                    'student id': student.studentId
                })

            class_info = []
            for c, study in clas:
                class_info.append({
                    'id': c.classId,
                    'class name': c.name,
                    'study': study.name,
                    'students': student_list
                })

            return class_info

    if request.method == "POST":
        name = request.json['name']
        study = request.json['study']

        cl = Class(name=name, studyId=study)
        db.session.add(cl)
        db.session.commit()

        return {'status': f'Class {name} for study {study} is created'}

    if request.method == "DELETE":
        cl = alchemist.get_class_by_id(class_id)
        cl.students = []
        db.session.commit()

        db.session.delete(cl)
        db.session.commit()

        return {'result': f'Class {class_id} has been deleted'}


@app.route('/meetings', methods=["GET", "POST"])
@app.route('/meetings/<meeting_id>', methods=["GET", "DELETE"])
def meetings_api(meeting_id=None):
    if request.method == "GET":
        if meeting_id == None:
            meetings = alchemist.get_all_meeting_info()
            all_meetings = []
            for meeting, course, teacher in meetings:
                all_meetings.append({
                    'Meeting Id': meeting.meetingId,
                    'Date': meeting.dateAndTime,
                    'Course': course.name,
                    'Teacher': teacher.name,
                })

            return all_meetings
        else:
            meeting = alchemist.get_meeting_by_id(meeting_id)
            course = alchemist.get_course_by_id(meeting.courseId)
            meeting_addition = alchemist.get_meeting_addition_by_id(meeting_id)

            students_scheduled = []
            for student in meeting.students_in_meeting:
                for study in student.studies:
                    students_scheduled.append({
                        'name': student.name,
                        'student_id': student.studentId,
                        'class': f'{study.studyId}: {study.name}'
                    })

            students_present = []
            present = alchemist.present_in_meeting(meeting_id)
            for student in present:
                s = alchemist.get_student_by_id(student.studentId)
                students_present.append({
                    'name': s.name,
                    'student_id': s.studentId
                })

            students_absent = []
            absent = alchemist.absent_in_meeting(meeting_id)
            for student in absent:
                s = alchemist.get_student_by_id(student.studentId)
                students_absent.append({
                    'name': s.name,
                    'student_id': s.studentId
                })

            students_called_off = []
            called_off = alchemist.called_off_meeting(meeting_id)
            for student in called_off:
                s = alchemist.get_student_by_id(student.studentId)
                students_called_off.append({
                    'name': s.name,
                    'student_id': s.studentId
                })

            student_replies = []
            for addition in meeting_addition:
                if addition.studentReply is not None:
                    student = alchemist.get_student_by_id(addition.studentId)
                    student_replies.append({
                        'student_id': student.studentId,
                        'student_name': student.name,
                        'reply': addition.studentReply
                    })

            classes = []
            for student in students_scheduled:
                classes.append(student['class'])

            unique_classes = set(classes)
            list_unique_classes = list(unique_classes)

            return jsonify(meeting_id=meeting.meetingId,
                           date=meeting.dateAndTime,
                           question=meeting.question,
                           course=course.name,
                           students_scheduled=students_scheduled,
                           students_present=students_present,
                           students_absent=students_absent,
                           students_called_off=students_called_off,
                           student_replies=student_replies,
                           classes_present=list_unique_classes)

    if request.method == "POST":
        date = datetime.strptime(request.json['date'], '%d/%m/%Y %H:%M')
        teacher = request.json['email']
        course = request.json['courseId']

        meeting = Meeting(dateAndTime=date, teacher=teacher, courseId=course)
        db.session.add(meeting)
        db.session.commit()

        return {'status': 'Meeting is aangemaakt'}

    if request.method == "DELETE":
        meeting = alchemist.get_meeting_by_id(meeting_id)
        meeting.students_in_meeting = []
        db.session.commit()
        db.session.delete(meeting)
        db.session.commit()

        return {'Message': f'Meeting {meeting_id} is deleted'}


@app.route('/teachers', methods=["POST", "GET"])
@app.route('/teachers/<teacher_id>', methods=["GET", "PUT", "DELETE"])
def teacher_api(teacher_id=None):
    if request.method == "GET":
        if teacher_id == None:
            teachers = alchemist.get_teachers()
            teacher_list = []
            for teacher in teachers:
                teacher_list.append({
                    'name': teacher.name,
                    'email': teacher.email,
                    'is admin': teacher.isAdmin
                })
            return teacher_list
        else:
            teacher = alchemist.get_teacher(teacher_id)
            meetings = alchemist.get_meeting_by_teacher(teacher_id)
            meeting_list = []
            for meeting, course in meetings:
                date = str(meeting.dateAndTime).split(' ')[0]
                time = str(meeting.dateAndTime).split(' ')[1]

                class_list = []

                for student in meeting.students_in_meeting:
                    for study in student.studies:
                        class_list.append({
                            'class': f'{study.studyId}: {study.name}'
                        })

                classes = []
                for clas in class_list:
                    classes.append(clas['class'])
                unique_classes = set(classes)
                list_unique_classes = list(unique_classes)

                meeting_list.append({
                    'meeting_id': meeting.meetingId,
                    'date': date,
                    'time': time,
                    'course': course.name,
                    'classes': list_unique_classes
                })

            return {
                'name': teacher.name,
                'email': teacher.email,
                'is admin': teacher.isAdmin,
                'meetings': meeting_list
            }

    if request.method == "POST":
        email = request.json['email']
        name = request.json['name']
        password = bcrypt.generate_password_hash(request.json['password'])
        is_admin = request.json['is admin']

        teacher = Teacher(email=email, name=name,
                          password=password, isAdmin=is_admin)
        db.session.add(teacher)
        db.session.commit()

        return {'status': f'Teacher {name} is created'}

    if request.method == "DELETE":
        teacher = alchemist.get_teacher(teacher_id)
        db.session.delete(teacher)
        db.session.commit()

        return {'status': f'Teacher {teacher.name} is deleted'}

    if request.method == "PUT":
        teacher = alchemist.get_teacher(teacher_id)
        teacher.email = request.json['email']
        teacher.name = request.json['name']
        teacher.password = bcrypt.generate_password_hash(
            request.json['password'])
        teacher.is_admin = request.json['is admin']

        db.session.commit()

        return {'status': f'Teacher {teacher.name} has been altered'}


@app.route('/students', methods=["GET", "POST"])
@app.route('/students/<student_id>', methods=["GET", "PUT", "DELETE"])
def students_api(student_id=None):
    if request.method == "GET":
        if student_id == None:
            students = alchemist.get_all_students()
            student_list = []
            for student in students:
                student_list.append({
                    'student_id': student.studentId,
                    'name': student.name
                })

            return student_list
        else:
            student = alchemist.get_student_by_id(student_id)
            # meetings = alchemist.get_meeting_by_student(student_id)

            studies = []
            for study in student.studies:
                studies.append({
                    'class_name': study.name,
                    'study_name': study.studyId
                })

            meeting_list = {
                'meetings_planned': [],
                'meetings_present': [],
                'meetings_absent': [],
                'meetings_called_off': [],
                'meetings_all': [],
            }

            all_meetings = alchemist.get_all_meeting_by_student(student_id)
            for meeting in all_meetings:
                date = str(meeting[4].dateAndTime).split(' ')[0]
                time = str(meeting[4].dateAndTime).split(' ')[1]
                meeting_list['meetings_all'].append({
                    'teacher': meeting[6].name,
                    'course': meeting[5].name,
                    'date': date,
                    'time': time,
                    'meeting_id': meeting[4].meetingId
                })
            planned_meetings = alchemist.get_planned_meeting_by_student(
                student_id)
            for meeting in planned_meetings:
                date = str(meeting[4].dateAndTime).split(' ')[0]
                time = str(meeting[4].dateAndTime).split(' ')[1]
                meeting_list['meetings_planned'].append({
                    'teacher': meeting[6].name,
                    'course': meeting[5].name,
                    'date': date,
                    'time': time,
                    'meeting_id': meeting[4].meetingId
                })
            present_meetings = alchemist.get_presence_student(
                student_id, 'present')
            for meeting in present_meetings:
                date = str(meeting[4].dateAndTime).split(' ')[0]
                time = str(meeting[4].dateAndTime).split(' ')[1]
                meeting_list['meetings_present'].append({
                    'teacher': meeting[6].name,
                    'course': meeting[5].name,
                    'date': date,
                    'time': time,
                    'meeting_id': meeting[4].meetingId
                })
            absent_meetings = alchemist.get_presence_student(
                student_id, 'absent')
            for meeting in absent_meetings:
                date = str(meeting[4].dateAndTime).split(' ')[0]
                time = str(meeting[4].dateAndTime).split(' ')[1]
                meeting_list['meetings_absent'].append({
                    'teacher': meeting[6].name,
                    'course': meeting[5].name,
                    'date': date,
                    'time': time,
                    'meeting_id': meeting[4].meetingId
                })
            called_off_meetings = alchemist.get_presence_student(
                student_id, 'called_off')
            for meeting in called_off_meetings:
                date = str(meeting[4].dateAndTime).split(' ')[0]
                time = str(meeting[4].dateAndTime).split(' ')[1]
                meeting_list['meetings_called_off'].append({
                    'teacher': meeting[5].name,
                    'course': meeting[5].name,
                    'date': date,
                    'time': time,
                    'meeting_id': meeting[4].meetingId
                })

            return jsonify(name=student.name,
                           student_number=student.studentId,
                           studies=studies,
                           all_meetings=meeting_list)

    if request.method == "POST":
        student_id = request.json['student id']
        name = request.json['name']
        password = bcrypt.generate_password_hash(request.json['password'])

        student = Student(studentId=student_id, name=name, password=password)
        db.session.add(student)
        db.session.commit()

        return {'status': f'Student {name} is created'}

    if request.method == "PUT":
        student = alchemist.get_student_by_id(student_id)
        student.student_id = request.json['student id']
        student.name = request.json['name']
        student.password = bcrypt.generate_password_hash(
            request.json['password'])

        db.session.commit()

        return {'status': f'Student {student.name} has been altered'}

    # DOES NOT WORK YET
    # CASCADING FAILURE ON MEETING_ADDITION
    # FIX CASCADED DELETE OF ROW
    if request.method == "DELETE":
        student = alchemist.get_student_by_id(student_id)
        db.session.delete(student)
        db.session.commit()

        return {'result': f'Student {student_id} has been deleted'}


@app.route('/get_latest_meeting_checkin')
def get_latest_meeting_checkin():
    student_id = request.args.get("studentId")
    dates_and_times = []
    meetings = db.session.query(meeting_addition).filter(
        meeting_addition.c.isPresent == 1, meeting_addition.c.studentId == student_id).all()

    for meeting in meetings:
        a_meeting = Meeting.query.filter_by(meetingId=meeting.meetingId).one()
        dates_and_times.append(a_meeting.dateAndTime)

    try:
        return jsonify({"date_and_time": max(dates_and_times)})
    except:
        return jsonify({"date_and_time": "Nooit ingecheckt"})


@app.route('/student-call-off-meeting/<meeting_id>', methods=["POST"])
def student_call_meeting_off(meeting_id):
    student_id = session['student_id']
    query_model.student_call_off(student_id, meeting_id)
    return redirect(url_for('student_screen', meeting_id=meeting_id))


@app.route('/teacher-call-off-meeting/<meeting_id>', methods=["POST"])
def teacher_call_meeting_off(meeting_id):
    meeting = alchemist.get_meeting_by_id(meeting_id)

    if meeting.students_in_meeting:
        for student in meeting.students_in_meeting:
            query_model.student_call_off(student.studentId, meeting_id)

    meeting.called_off = True
    db.session.commit()

    return redirect(url_for('teacher_menu'))


@app.route('/student-response/<meeting_id>', methods=["POST"])
def student_reply(meeting_id):
    student_id = session["student_id"]
    reply = request.form['student-response']
    query_model.student_reply(meeting_id, student_id, reply)
    return redirect(url_for('student_screen'))


@app.route('/beamer-student-call-off/<student_id>/<meeting_id>', methods=["POST"])
def beamer_student_call_off(student_id, meeting_id):
    query_model.student_call_off(student_id, meeting_id)
    return {'status': 'student hasd been called off'}


@app.route('/beamer-student-absent/<student_id>/<meeting_id>', methods=["POST"])
def beamer_student_absent(student_id, meeting_id):
    query_model.student_absent(student_id, meeting_id)
    return {'status': 'student hasd been put on absent'}


@app.route('/end-meeting/<meeting_id>', methods=["POST"])
def end_meeting(meeting_id):
    meeting = alchemist.end_meeting(meeting_id)
    meeting.finished = True
    db.session.commit()


@app.route('/student-lookup/<student_id>', methods={"GET"})
def student_info(student_id, student_name):
    student_id = alchemist.get_all_students(student_id)
    student_name = alchemist.get_all_students(student_name)

    db.session.commit()
    return redirect(url_for('student_info', student_id=student_id, student_name=student_name))


@app.route('/create-meeting', methods=["POST"])
def create_meeting():
    data = request.get_json()

    teacher = data['teacher']
    course = data['course']
    question = data['question']
    date = data['dateAndTime']
    date_and_time = datetime.strptime(date, '%Y-%m-%d %H:%M')

    meeting = Meeting(dateAndTime=date_and_time,
                      question=question,
                      teacher=teacher,
                      courseId=course
                      )
    db.session.add(meeting)
    db.session.commit()

    last_entry = db.session.query(Meeting).order_by(
        Meeting.meetingId.desc()).first()

    # Adds whole class
    classes = data['classes']
    for clas in classes:
        c = alchemist.get_class_by_id(clas)
        for student in c.students:
            query_model.add_student_to_meeting(
                student.studentId, last_entry.meetingId)

    # Adds single student
    students = data['students']
    for student in students:
        stud = db.session.query(Student).filter(
            Student.studentId == student).first()
        query_model.add_student_to_meeting(
            stud.studentId, last_entry.meetingId)

    return {'status': 'meeting has been created'}


@app.route('/student-filter/<value>', methods=["GET"])
@login_required
def student_filter_create_meeting_screen(value):
    students = alchemist.get_student_by_id_or_name(value)
    student_list = []
    for student in students:
        student_list.append({
            'student_id': student.studentId,
            'name': student.name
        })

    # print(student_list)
    return jsonify(student_list)

    return redirect(url_for('student_screen', meeting_id=meeting_id))


@app.route('/remove_student_from_class', methods=['GET', 'POST'])
def remove_student_from_class():
    student_id = request.args.get("studentId")
    class_id = request.args.get("classId")

    execute_model = query_model()
    delete_query = f"DELETE FROM class_to_student_table WHERE studentId = {int(student_id)} AND classId = {int(class_id)}"

    execute_model.execute_update(delete_query)

    return Response('{"message": "Gebruiker is uit de klas verwijderd"}', status=200, mimetype='application/json')


@app.route('/get_all_studies')
def get_all_studies():
    studies = []

    for study in Study.query.all():
        a_study = {
            "studyId": study.studyId,
            "name": study.name
        }
        studies.append(a_study)

    return jsonify(studies)


@app.route('/add_student_to_class', methods=["GET", "POST"])
def add_student_to_class():
    execute_model = query_model()

    student_id = request.args.get("studentId")
    class_id = request.args.get("classId")

    query = f"INSERT INTO class_to_student_table (studentId, classId) VALUES ({student_id}, {class_id})"

    execute_model.execute_update(query)

    return Response('{"message": "Gebruiker is toegevoegd aan de klas", "status_category":"success"}', status=200,
                    mimetype='application/json')


@app.route("/edit_database_row", methods=["GET", "POST"])
def edit_database_row():
    execute_model = query_model()
    table_name = request.args.get("table_name")

    column = request.args.get("column")
    value = request.args.get("value")

    condition_column = request.args.get("condition_column")
    condition_value = request.args.get("condition_value")

    query = f"UPDATE {table_name} SET {column} = '{value}' WHERE {condition_column} = {condition_value}"

    execute_model.execute_update(query)

    return Response('{"message": "Informatie is aangepast", "status_category":"success"}', status=200,
                    mimetype='application/json')


@app.route("/add_student_account", methods=["GET", "POST"])
def add_student_account():
    execute_model = query_model()

    student_id = request.args.get("studentId")
    student_name = request.args.get("name")
    password = request.args.get("password")
    class_id = request.args.get("classId")

    a_student = Student(studentId=int(student_id), name=student_name,
                        password=bcrypt.generate_password_hash(password))
    db.session.add(a_student)
    db.session.commit()

    query = f"INSERT INTO class_to_student_table (studentId, classId) VALUES ({student_id}, {class_id})"

    print(query)
    execute_model.execute_update(query)

    return Response('{"message": "Gebruiker is aangemaakt", "status_category":"success"}', status=200,
                    mimetype='application/json')


@app.route("/create_class", methods=["GET", "POST"])
def create_class():
    class_name = request.args.get("name")
    study_id = request.args.get("studyId")

    try:
        Class.query.filter((Class.name == f'{class_name}') & (
                Class.studyId == f'{study_id}')).one()
        return Response(
            '{"message": "Er bestaat al een klas met die titel op deze studie! Kies een andere klastitel.", "status_category":"danger"}',
            status=200,
            mimetype='application/json')
    except:
        new_class = Class(name=class_name, studyId=study_id)
        db.session.add(new_class)
        db.session.commit()
        db.session.refresh(new_class)

        return jsonify({"message": "Klas is aangemaakt!", "status_category": "success", "class_id": new_class.classId})


@app.route("/create_teacher", methods=["POST"])
def create_teacher():
    email = request.args.get("email")
    name = request.args.get("name")
    password = request.args.get("password")
    is_admin = request.args.get("admin")

    if is_admin == "true":
        is_admin = True
    else:
        is_admin = False

    print(f"Email: {email}, name: {name}, Password: {password}, Is_admin: {is_admin}")

    new_teacher = Teacher(email=email, name=name, password=bcrypt.generate_password_hash(password), isAdmin=is_admin)
    db.session.add(new_teacher)
    db.session.commit()

    return jsonify({"message": "Leraar is aangemaakt", "status_category": "success"})


# @app.route("/get-latest-checkin", methods=["GET", "POST"])
# def get_latest_checkin():
#     student_id = request.json.get("studentid", 1)
#     dates_and_times = []
#     meetings = db.session.query(meeting_addition).filter(meeting_addition.c.IsPresent == 1, meeting_addition.c.studentId == student_id).all()
#
#     for meeting in meetings:
#         a_meeting = Meeting.query.filter_by(meetingId=meeting.meetingId).one()
#         dates_and_times.append(a_meeting.dateAndTime)
#
#         try:
#             return jsonify({"date_and_time": max(dates_and_times)})
#         except:
#             return jsonify({"date_and_time": "Nooit ingecheckt"})