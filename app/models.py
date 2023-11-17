from app import db, app
from flask_login import UserMixin
import random, string


meeting_addition = db.Table('meeting_addition',
                            db.Column('meetingId', db.Integer, db.ForeignKey(
                                'meeting.meetingId'), primary_key=True),
                            db.Column('studentId', db.Integer, db.ForeignKey(
                                'student.studentId'), primary_key=True),
                            db.Column('isPresent', db.Integer),
                            db.Column('studentReply', db.Text)
                            )

class_to_student_table = db.Table('class_to_student_table',
                                  db.Column('studentId', db.Integer, db.ForeignKey(
                                      'student.studentId'), primary_key=True),
                                  db.Column('classId', db.Integer, db.ForeignKey(
                                      'class.classId'), primary_key=True),
                                  )


class Student(db.Model, UserMixin):
    studentId = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(60), nullable=False)

    studies = db.relationship('Class', secondary=class_to_student_table,
                              backref='class_with_student', lazy='dynamic',
                              overlaps='students_in_class')
    meetings = db.relationship(
        'Meeting', secondary=meeting_addition, backref='meeting_with_student',
        lazy='dynamic', overlaps='students_in_meeting')

    def get_id(self):
        return self.studentId

    def get_reset_token(self):
        token = f'{self.studentId}'
        if len(token) != 40:
            token += string.ascii_lowercase
        return token
        
    def __repr__(self):
        return f"Student('StudentId: {self.studentId}', Name: '{self.name}')"


class Class(db.Model):
    classId = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(10), nullable=False)
    studyId = db.Column(db.String(10), db.ForeignKey(
        'study.studyId'), nullable=False)

    students = db.relationship(
        'Student', secondary=class_to_student_table,
        backref='students_in_class', lazy='dynamic',
        overlaps="class_with_student,studies", cascade='delete')

    def __repr__(self):
        return f"Class('{self.classId}', '{self.name}', '{self.studyId}')"


class Study(db.Model):
    studyId = db.Column(db.String(10), primary_key=True)
    name = db.Column(db.String(50))

    def __repr__(self):
        return f"Study('{self.studyId}', '{self.name}')"


class Teacher(db.Model, UserMixin):
    email = db.Column(db.String(50), primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(60), nullable=False)
    isAdmin = db.Column(db.Boolean, nullable=True)

    def get_id(self):
        return self.email

    def get_reset_token(self, expires_sec=3600):
        token = f'{self.email}'
        if len(token) != 40:
            token += string.ascii_lowercase

        return token

    def __repr__(self):
        return f"Teacher('{self.email}', '{self.name}', '{self.isAdmin}')"


class Course(db.Model):
    courseId = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return f"Course('{self.courseId}', '{self.name}')"


class Meeting(db.Model):
    meetingId = db.Column(db.Integer, primary_key=True, autoincrement=True)
    dateAndTime = db.Column(db.DateTime, nullable=False)
    question = db.Column(db.String(1000))
    called_off = db.Column(db.Boolean, default=False)
    finished = db.Column(db.Boolean, default=False)

    teacher = db.Column(db.String(50), db.ForeignKey(
        'teacher.email'), nullable=False)
    courseId = db.Column(db.Integer, db.ForeignKey(
        'course.courseId'), nullable=False)

    students_in_meeting = db.relationship(
        'Student', secondary=meeting_addition, backref='students_in_meeting',
        cascade='delete', lazy='dynamic',
        overlaps='meeting_with_student')

    def __repr__(self):
        return f"""Meeting('meetingId: {self.meetingId}', 
                dateAndTime: '{self.dateAndTime}', 
                teacher: '{self.teacher}', courseId: '{self.courseId}')"""
