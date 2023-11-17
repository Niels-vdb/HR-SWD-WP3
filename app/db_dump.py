from app import db, fake, bcrypt, app
from app.models import *


@app.route('/database-dump')
def database_dump():
    db.create_all()

    password = bcrypt.generate_password_hash('werkplaats3')
    teachers = ['Tjidde Maijer', 'Mark Otting', 'Jelle van der Loo',
                'Veysel Altinok', 'Diederik de Vries', 'Eva Schaap', 'Gayatri Goyal']

    for teacher in teachers:
        fname = teacher.lower().split(' ')[0]
        lname = teacher.lower().split(' ')[-1]
        email = f'{fname[0]}.{lname}@hr.nl'
        t = Teacher(email=email, name=teacher,
                    password=password, isAdmin=False)
        db.session.add(t)
        db.session.commit()

    for i in range(1000):
        name = fake.name()
        s = Student(name=name, password=password)
        db.session.add(s)
        db.session.commit()

    studies = ['SWD Software Development', 'IOT Internet Of Things', 'LO Leraren Opleiding',
               'PABO Pedagogische Academie voor het Basisonderwijs', 'DA Database Analytics', 
               'CC Crossmediale Communicatie', 'ISM ITC Service Management', 'SW Social Work',
                'SA Sales & Accountmanagement', 'SFD Sociaal Financiële Dienstverlening']
    for study in studies:
        id = study.split(' ', 1)[0]
        name = study.split(' ', 1)[1]
        s = Study(studyId=id, name=name)
        db.session.add(s)
        db.session.commit()

    courses = ['Nederlands', 'Engels', 'Wiskunde', 'UX', 'Professionele Vorming',
               'Studie Loopbaan Coaching', 'Werkplaats', 'Persoonlijk gesprek', 'Programming Essentials']
    for course in courses:
        c = Course(name=course)
        db.session.add(c)
        db.session.commit()

    classes = ['1a', '1b', '1c', '1d', '2a', '2b',
               '2c', '3a', '3b', '3c', '4a', '4b', '4c']
    for clas in classes:
        c = Class(name=clas, studyId='SWD')
        db.session.add(c)
        db.session.commit()

    for clas in classes:
        c = Class(name=clas, studyId='IOT')
        db.session.add(c)
        db.session.commit()

    for clas in classes:
        c = Class(name=clas, studyId='LO')
        db.session.add(c)
        db.session.commit()

    for clas in classes:
        c = Class(name=clas, studyId='PABO')
        db.session.add(c)
        db.session.commit()

    i = 1
    j = 31
    for clas in range(1, 66):
        c = db.session.query(Class).filter(Class.classId == clas).first()
        if j > 1000:
            break
        for student in range(i, j):
            s = db.session.query(Student).filter(
                Student.studentId == student).first()
            s.studies.append(c)
            db.session.commit()
        i += 30
        j += 30

    return {'status': 'Database has been filled'}
