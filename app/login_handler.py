from app import app, bcrypt, login_manager, db, mail
from app.models import Student, Teacher
from flask import request, session, render_template, flash, redirect, url_for
from flask_login import login_user, login_required, logout_user, current_user
from app.forms import LoginForm, RequestResetForm, ResetPasswordForm
from app.alchemist import SqliteQueries as query_model
from flask_mail import Message
import re

def get_user_role(user_object):
    try:
        if user_object.email:
            if current_user.isAdmin == 1:
                return "admin"
            else:
                return "teacher"
    except:
        return "student"


@login_manager.user_loader
def load_user(user_id):
    student = Student.query.get(user_id)
    teacher = Teacher.query.get(user_id)

    if student:
        return student
    elif teacher:
        return teacher


@app.route('/', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        student = Student.query.filter_by(studentId=form.id.data).first()
        teacher = Teacher.query.filter_by(email=form.id.data).first()

        if student and bcrypt.check_password_hash(student.password, form.password.data):
            login_user(student)
            session['student_id'] = student.studentId
            session['student_name'] = student.name
            if request.args.get('next') == None:
                session['long_alert'] = True
                flash('Login goedgekeurd!', 'success')
                return redirect(url_for('student_screen'))
            else:
                meeting_id = str(request.args.get('next'))
                session['meeting_id'] = meeting_id[9:]
                query_model.student_check_in(
                    student.studentId, meeting_id[9:])
                flash('Login goedgekeurd!', 'success')
                return redirect(url_for('student_screen', meeting_id=meeting_id[9:]))
        elif teacher and bcrypt.check_password_hash(teacher.password, form.password.data):
            login_user(teacher)
            session['teacher_id'] = teacher.email
            session['teacher_name'] = teacher.name
            session['teacher_admin'] = teacher.isAdmin
            next_url = request.args.get('next')
            if next_url:
                match next_url[1:]:
                    case 'bijeenkomst-aanmaken':
                        return redirect(url_for('make_meeting_screen'))
                    case 'student-lookup':
                        return redirect(url_for('student_search'))
                    case 'manage_account':
                        return redirect(url_for('manage_account'))
            
            flash('Login goedgekeurd!', 'success')
            return redirect(url_for('teacher_menu'))
        else:
            flash('Check je studentnummer en/of wachtwoord!', 'danger')

    return render_template('login.html', title='Login', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


def send_reset_email(user):
    if isinstance(user, Teacher):
        token = user.get_reset_token()
        message = Message('Aanvraag voor nieuw wachtwoord',
                        sender='werkplaats743@gmail.com', recipients=[user.email])

        message.body = f'''Om je wachtwoord te reseten, gebruik de volgende link.
{url_for('reset_password', token=token, _external=True)}
Als jij hier niet om had gevraagt kan je deze mail negeren.
'''
        mail.send(message)

    if isinstance(user, Student):
        token = user.get_reset_token()
        email = f'{str(user.studentId)}@hr.nl'
        message = Message('Aanvraag voor nieuw wachtwoord',
                        sender='werkplaats743@gmail.com', recipients=[email])

        message.body = f'''Om je wachtwoord te reseten, gebruik de volgende link.
{url_for('reset_password', token=token, _external=True)}
Als jij hier niet om had gevraagt kan je deze mail negeren.
'''
        mail.send(message)


@app.route('/request-password', methods=["GET", "POST"])
def request_password():
    form = RequestResetForm()
    if form.validate_on_submit():
        student = db.session.query(Student).filter(
            Student.studentId == form.input.data).first()
        teacher = db.session.query(Teacher).filter(
            Teacher.email == form.input.data).first()
        if student is not None:
            send_reset_email(student)
        send_reset_email(teacher)
        
        # send_reset_email(student)
        flash('Je hebt een email ontvangen met instructies om je wachtwoord te wijzigen.', 'info')
        return redirect(url_for('login'))
    return render_template('request-password.html', form=form, title='Nieuw Wachtwoord')


@app.route('/reset-password/<token>', methods=["GET", "POST"])
def reset_password(token):
    encrypt =  re.findall('[0-9]', token)
    decrypt = ''.join(encrypt)

    student = db.session.query(Student).filter(Student.studentId == decrypt).first()
    teacher = db.session.query(Teacher).filter(Teacher.email == decrypt).first()
    if student is None and teacher is None:
        flash('Je hebt een ongeldige of vervallen token, probeer opnieuw.', 'danger')
        return redirect(url_for('request_password'))
    
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data)
        if teacher:
            teacher.password = hashed_password
            db.session.commit()
            flash('Je wachtwoord is veranderd, je kan weer inloggen.', 'info')
            return redirect(url_for('login'))
        else:
            student.password = hashed_password
            db.session.commit()
            flash('Je wachtwoord is veranderd, je kan weer inloggen.', 'info')
            return redirect(url_for('login'))

    return render_template('reset-password.html', form=form)
