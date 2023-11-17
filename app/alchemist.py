from app import db
from app.models import *
import sqlite3
import os
from typing import NamedTuple


class StudentPresenceCount(NamedTuple):
    studentid: int
    count: int


class Alchemist:
    def get_all_students():
        query = db.session.query(Student).all()
        return query

    def get_student_by_id(student_id):
        query = db.session.query(Student).filter(
            Student.studentId == student_id).first()
        return query

    def get_student_by_id_or_name(value):
        query = db.session.query(Student).filter(
            (Student.studentId.like(f'%{value}%')) | (Student.name.like(f'%{value}%'))).all()
        return query

    def get_student_info(student_id):
        query = db.session.query(Student, Class, Study).join(Class).join(Study) \
            .filter(Student.studentId == student_id).first()
        return query

    def present_in_meeting(meeting_id):
        query = db.session.query(meeting_addition).filter(meeting_addition.c.isPresent == 1,
                                                          meeting_addition.c.meetingId == meeting_id).all()
        return query

    def absent_in_meeting(meeting_id):
        query = db.session.query(meeting_addition)\
            .filter(meeting_addition.c.isPresent == 0,
                    meeting_addition.c.meetingId == meeting_id).all()
        return query

    def called_off_meeting(meeting_id):
        query = db.session.query(meeting_addition)\
            .filter(meeting_addition.c.isPresent == 2,
                    meeting_addition.c.meetingId == meeting_id).all()
        return query

    def end_meeting(meeting_id):
        query = db.session.query(Meeting).filter(
            Meeting.meetingId == meeting_id).first()
        return query

    def teacher_meeting_info(teacher_id):
        query = db.session.query(Meeting, Course).select_from(Meeting).join(Course) \
            .filter(Meeting.teacher == teacher_id,
                    Meeting.called_off == False,
                    Meeting.finished == False)\
            .order_by(Meeting.dateAndTime).all()
        return query

    def get_meeting_by_id(meeting_id):
        query = db.session.query(Meeting).filter(
            Meeting.meetingId == meeting_id).first()
        return query

    def get_meeting_addition_by_id(meeting_id):
        query = db.session.query(meeting_addition) \
            .filter(meeting_addition.c.meetingId == meeting_id).all()
        return query

    def get_course_by_id(course_id):
        query = db.session.query(Course).filter(
            Course.courseId == course_id).first()
        return query

    def get_all_meeting_by_student(student_id):
        query = db.session.query(meeting_addition, Meeting, Course, Teacher) \
            .select_from(meeting_addition) \
            .join(Meeting).join(Course).join(Teacher) \
            .filter(meeting_addition.c.studentId == student_id) \
            .order_by(Meeting.dateAndTime)\
            .all()
        return query

    def get_planned_meeting_by_student(student_id):
        query = db.session.query(meeting_addition, Meeting, Course, Teacher) \
            .select_from(meeting_addition) \
            .join(Meeting).join(Course).join(Teacher) \
            .filter(meeting_addition.c.studentId == student_id,
                    meeting_addition.c.isPresent != 1,
                    meeting_addition.c.isPresent != 2,
                    Meeting.finished == False) \
            .order_by(Meeting.dateAndTime)\
            .all()
        return query

    def get_presence_student(student_id, value):
        match value:
            case 'present':
                query = db.session.query(meeting_addition, Meeting, Course, Teacher) \
                    .select_from(meeting_addition) \
                    .join(Meeting).join(Course).join(Teacher) \
                    .filter(meeting_addition.c.studentId == student_id,
                            meeting_addition.c.isPresent == 1) \
                    .order_by(Meeting.dateAndTime)\
                    .all()
                return query
            case 'absent':
                query = db.session.query(meeting_addition, Meeting, Course, Teacher) \
                    .select_from(meeting_addition) \
                    .join(Meeting).join(Course).join(Teacher) \
                    .filter(meeting_addition.c.studentId == student_id,
                            meeting_addition.c.isPresent == 0) \
                    .order_by(Meeting.dateAndTime)\
                    .all()
                return query
            case 'called_off':
                query = db.session.query(meeting_addition, Meeting, Course, Teacher) \
                    .select_from(meeting_addition) \
                    .join(Meeting).join(Course).join(Teacher) \
                    .filter(meeting_addition.c.studentId == student_id,
                            meeting_addition.c.isPresent == 2) \
                    .order_by(Meeting.dateAndTime)\
                    .all()
                return query

    def get_meeting_info_by_id(self, meeting_id):
        query = db.session.query(meeting_addition, Meeting, Course, Teacher) \
            .select_from(meeting_addition) \
            .join(Meeting).join(Course).join(Teacher) \
            .filter(meeting_addition.c.meetingId == meeting_id) \
            .first()
        return query

    def get_meeting_by_id(meeting_id):
        query = db.session.query(Meeting) \
            .filter(Meeting.meetingId == meeting_id) \
            .first()
        return query

    def get_meeting_by_teacher(teacher_id):
        query = db.session.query(Meeting, Course)\
            .join(Course)\
            .order_by(Meeting.dateAndTime)\
            .filter(Meeting.teacher == teacher_id,
                    Meeting.called_off == 0,
                    Meeting.finished == False)\
            .all()
        return query

    def get_all_meeting_info():
        query = db.session.query(Meeting, Course, Teacher) \
            .join(Course).join(Teacher).all()
        return query

    def get_all_classes():
        query = db.session.query(Class, Study).join(Study).all()
        return query

    def get_class(class_id):
        query = db.session.query(Class, Study).join(Study) \
            .filter(Class.classId == class_id).first()
        return query

    def get_class_by_id(class_id):
        query = db.session.query(Class).filter(
            Class.classId == class_id).first()
        return query

    def get_students_in_class(class_id):
        query = db.session.query(Class).filter(
            Class.classId == class_id).first()
        return query

    def get_teachers():
        query = db.session.query(Teacher).all()
        return query

    def get_teacher(teacher_id):
        query = db.session.query(Teacher).filter(
            Teacher.email == teacher_id).first()
        return query

    def get_studies():
        query = db.session.query(Study).all()
        return query

    def get_courses():
        query = db.session.query(Course).all()
        return query

    def get_finished_meetings(teacher_id):
        query = db.session.query(Meeting).filter(
            Meeting.teacher == teacher_id, Meeting.finished == True).all()
        return query


class SqliteQueries:
    def __init__(self):
        self.DATABASE_FILE = os.path.join('instance/site.db')

    def execute_update(self, sql_query):
        conn = sqlite3.connect(self.DATABASE_FILE)
        cursor = conn.cursor()
        cursor.row_factory = sqlite3.Row
        cursor.execute(sql_query)
        conn.commit()

    def add_student_to_meeting(student_id, meeting_id):
        query = f'''INSERT INTO meeting_addition 
                    (meetingId, studentId, isPresent)
                    VALUES({meeting_id}, {student_id}, 0)'''

        conn = sqlite3.connect(os.path.join('instance/site.db'))
        cursor = conn.cursor()
        cursor.row_factory = sqlite3.Row
        cursor.execute(query)
        conn.commit()

    def student_check_in(student_id, meeting_id):
        query = f'''UPDATE meeting_addition 
                    SET isPresent = 1 
                    WHERE studentId = {student_id} 
                    AND meetingId = {meeting_id}'''

        conn = sqlite3.connect(os.path.join('instance/site.db'))
        cursor = conn.cursor()
        cursor.row_factory = sqlite3.Row
        cursor.execute(query)
        conn.commit()

    def student_call_off(student_id, meeting_id):
        query = f'''UPDATE meeting_addition 
                    SET isPresent = 2 
                    WHERE studentId = {student_id} 
                    AND meetingId = {meeting_id};'''

        conn = sqlite3.connect(os.path.join('instance/site.db'))
        cursor = conn.cursor()
        cursor.row_factory = sqlite3.Row
        cursor.execute(query)
        conn.commit()

    def student_absent(student_id, meeting_id):
        query = f'''UPDATE meeting_addition 
                    SET isPresent = 0 
                    WHERE studentId = {student_id} 
                    AND meetingId = {meeting_id};'''

        conn = sqlite3.connect(os.path.join('instance/site.db'))
        cursor = conn.cursor()
        cursor.row_factory = sqlite3.Row
        cursor.execute(query)
        conn.commit()

    def student_reply(meeting_id, student_id, reply):
        query = f'''UPDATE meeting_addition
                    SET studentReply = "{reply}"
                    WHERE studentId = {student_id}
                    AND meetingId = {meeting_id}'''
        conn = sqlite3.connect(os.path.join('instance/site.db'))
        cursor = conn.cursor()
        cursor.row_factory = sqlite3.Row
        cursor.execute(query)
        conn.commit()

    def show_studentlist(studentId):
        query = f''' SELECT * FROM student WHERE studentId = {studentId}; '''
        conn = sqlite3.connect(os.path.join('instance/site.db'))
        cursor = conn.cursor()
        cursor.execute(query)
        result = cursor.fetchall()
        conn.close()

        return result

    @staticmethod
    def get_students():
        query = "SELECT student.studentId, student.name FROM student;"
        return SqliteQueries.execute_query(query)

    @staticmethod
    def execute_query(query, params=None):
        params = tuple() if params is None else params
        conn = sqlite3.connect(os.path.join('instance/site.db'))
        cursor = conn.cursor()
        cursor.execute(query, params)
        result = cursor.fetchall()
        conn.close()

        return result

    @staticmethod
    def count_meeting_general():
        query = """
        SELECT student.studentId, student.name, meeting_addition.isPresent, count(meeting_addition.meetingId)
        FROM meeting_addition, student
        WHERE student.studentId = meeting_addition.studentId
        GROUP BY student.studentId, meeting_addition.isPresent """
        conn = sqlite3.connect(os.path.join('instance/site.db'))
        cursor = conn.cursor()
        cursor.execute(query)
        result = cursor.fetchall()
        conn.close()

        return result

    @staticmethod
    def count_meeting_presence(student_id: int) -> int:
        query = """
        SELECT student.studentId, count(meeting_addition.meetingId)
        FROM meeting_addition, student
        WHERE student.studentId = meeting_addition.studentId AND student.studentId = ? AND meeting_addition.isPresent = 0
        GROUP BY student.studentId"""

        allresults = SqliteQueries.execute_query(query, (student_id,))
        if len(allresults) > 0:
            return [count for _, count in allresults][0]
        return 0

    @staticmethod
    def count_meeting_absence(student_id: int) -> int:
        query = """SELECT student.studentId, count(meeting_addition.meetingId)
        FROM meeting_addition, student
        WHERE student.studentId = meeting_addition.studentId AND student.studentId = ? AND meeting_addition.isPresent = 1
        GROUP BY student.studentId"""

        allresults = SqliteQueries.execute_query(query, (student_id,))
        if len(allresults) > 0:
            return [count for _, count in allresults][0]
        return 0

    @staticmethod
    def count_meeting_checked_out(student_id: int) -> int:
        query = """ SELECT student.studentId, count(meeting_addition.meetingId)
        FROM meeting_addition, student
        WHERE student.studentId = meeting_addition.studentId AND student.studentId = ? AND meeting_addition.isPresent = 2
        GROUP BY student.studentId """

        allresults = SqliteQueries.execute_query(query, (student_id,))
        if len(allresults) > 0:
            return [count for _, count in allresults][0]
        return 0

    @staticmethod
    def get_name_for_student_id(studentid: int):
        query = """
        SELECT student.name 
        FROM student
        WHERE student.studentId = ?
        LIMIT 1
        """

        return SqliteQueries.execute_query(query, (studentid,))[0][0]

    @staticmethod
    def count_no_of_meetings_for_student_id(student_id: int) -> int:
        query = """
        SELECT count(*) FROM meeting_addition WHERE meeting_addition.studentId = ?;
        """
        return SqliteQueries.execute_query(query, (student_id,))[0][0]

    @staticmethod
    def get_course_presence(student_id, course_name):
        query = """ 
                SELECT count(meeting_addition.meetingId)
                FROM meeting_addition,  meeting, student, course
                WHERE student.studentId = meeting_addition.studentId AND
                student.studentId = ? AND
                meeting_addition.isPresent = 0 AND
                meeting.courseId = course.courseId AND
                meeting.meetingId = meeting_addition.meetingId AND
                course.name = ?"""
        result = SqliteQueries.execute_query(query, (student_id,course_name))
        if result:
            return result[0][0]
        return 0

    @staticmethod
    def get_course_absence(student_id, course_name):
        query = """    
                SELECT count(meeting_addition.meetingId)
                FROM meeting_addition,  meeting, student, course
                WHERE student.studentId = meeting_addition.studentId AND
                student.studentId = ? AND
                meeting_addition.isPresent = 1 AND
                meeting.courseId = course.courseId AND
                meeting.meetingId = meeting_addition.meetingId AND
                course.name = ?"""
        result = SqliteQueries.execute_query(query, (student_id, course_name))
        if result:
            return result[0][0]
        return 0

    @staticmethod
    def get_course_checked_out(student_id, course_name):
        query = """ 
                SELECT count(meeting_addition.meetingId)
                FROM meeting_addition,  meeting, student, course
                WHERE student.studentId = meeting_addition.studentId AND
                student.studentId = ? AND
                meeting_addition.isPresent = 2 AND
                meeting.courseId = course.courseId AND
                meeting.meetingId = meeting_addition.meetingId AND
                course.name = ?"""
        result = SqliteQueries.execute_query(query, (student_id, course_name))
        if result:
            return result[0][0]
        return 60





