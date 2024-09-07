from . import db, session, Base
from sqlalchemy import Table
from sqlalchemy.orm import relationship
from flask_jwt_extended import create_access_token, create_refresh_token
from datetime import timedelta, datetime
from passlib.hash import bcrypt


laba_group_association = Table('laba_group_association', Base.metadata,
    db.Column('laba_id', db.Integer, db.ForeignKey('labs.id')),
    db.Column('group_id', db.Integer, db.ForeignKey('groups.id'))
)

user_group_association = Table('user_group_association', Base.metadata,
    db.Column('user_id', db.Integer, db.ForeignKey('students.id')),
    db.Column('group_id', db.Integer, db.ForeignKey('groups.id'))
)



class SectionLaba(Base):
    __tablename__ = 'sections_labs'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)

    def __init__(self, **kwargs):
        self.name = kwargs.get('name')

    def save(self):
        try:
            session.add(self)
            session.commit()
        except Exception:
            session.rollback()
            raise

    @property
    def pk(self):
        return self.id




class Laba(Base):
    __tablename__ = 'labs'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    is_active = db.Column(db.Boolean)
    groups = relationship("Group", secondary=laba_group_association, back_populates="labs")
    section_id = db.Column(db.Integer, db.ForeignKey('sections_labs.id'))
    section = relationship("SectionLaba")
    test = relationship("Test", back_populates="laba")



    def __init__(self, **kwargs):
        self.name = kwargs.get('name')
        self.is_active = True
        self.section_id = kwargs.get('section_id')

    def save(self):
        try:
            session.add(self)
            session.commit()
        except Exception:
            session.rollback()
            raise



    @property
    def pk(self):
        return self.id
    
    @property
    def link(self):
        return f"http://www.infochemistryweb.ru/files/{self.id}.pdf"



class Group(Base):
    __tablename__ = 'groups'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    creator_id = db.Column(db.Integer, db.ForeignKey('students.id'))
    creator = relationship("Student")
    users = relationship("Student", secondary=user_group_association, back_populates="groups")
    labs = relationship("Laba", secondary=laba_group_association, back_populates="groups")

    

    def __init__(self, **kwargs):
        self.name = kwargs.get('name')
        self.creator_id = kwargs.get('creator_id')


    def save(self):
        try:
            session.add(self)
            session.commit()
        except Exception:
            session.rollback()
            raise


    @property
    def pk(self):
        return self.id



class Test(Base):
    __tablename__ = 'tests'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    laba_id = db.Column(db.Integer, db.ForeignKey('labs.id'))
    attempts = db.Column(db.Integer)

    laba = relationship("Laba", back_populates="test")
    questions = relationship("TestQuestion", back_populates="test")
    submits = relationship("SubmitTest", back_populates="test")


    def __init__(self, **kwargs):
        self.name = kwargs.get('name')
        self.laba_id = kwargs.get('laba_id')
        self.attempts = kwargs.get("attempts")


    def save(self):
        try:
            session.add(self)
            session.commit()
        except Exception:
            session.rollback()
            raise
        

    @property
    def pk(self):
        return self.id


class TestQuestion(Base):
    __tablename__ = 'tests_questions'

    id = db.Column(db.Integer, primary_key=True)
    test_id = db.Column(db.Integer, db.ForeignKey('tests.id'))
    question = db.Column(db.String)
    image = db.Column(db.String)

    test = relationship("Test", back_populates="questions")
    answers = relationship("TestAnswer", back_populates="question")


    def __init__(self, **kwargs):
        self.test_id = kwargs.get('test_id')
        self.question = kwargs.get('question')
        self.image = kwargs.get('image')


    def save(self):
        try:
            session.add(self)
            session.commit()
        except Exception:
            session.rollback()
            raise
        

    @property
    def pk(self):
        return self.id



class TestAnswer(Base):
    __tablename__ = 'tests_answers'

    id = db.Column(db.Integer, primary_key=True)
    question_id = db.Column(db.Integer, db.ForeignKey('tests_questions.id'))
    answer = db.Column(db.String)
    flag = db.Column(db.Boolean)

    question = relationship("TestQuestion", back_populates="answers")


    def __init__(self, **kwargs):
            self.answer = kwargs.get('answer')
            self.question_id = kwargs.get('question_id')
            self.flag = kwargs.get('flag')


    def save(self):
        try:
            session.add(self)
            session.commit()
        except Exception:
            session.rollback()
            raise
        

    @property
    def pk(self):
        return self.id



class SubmitTest(Base):
    __tablename__ = 'submit_test'

    id = db.Column(db.Integer, primary_key=True)
    score = db.Column(db.Integer)
    max_score = db.Column(db.Integer)
    test_id = db.Column(db.Integer, db.ForeignKey('tests.id'))
    student_id = db.Column(db.Integer, db.ForeignKey('students.id'))
    date = db.Column(db.DateTime(), default=datetime.utcnow)



    student = relationship("Student", back_populates="submit_tests")
    test = relationship("Test", back_populates="submits")


    def __init__(self, **kwargs):
            self.score = kwargs.get('score')
            self.max_score = kwargs.get('max_score')
            self.test_id = kwargs.get('test_id')
            self.student_id = kwargs.get('student_id')



    def save(self):
        try:
            session.add(self)
            session.commit()
        except Exception:
            session.rollback()
            raise
        

    @property
    def pk(self):
        return self.id


    @property
    def pk_test(self):
        return self.test_id
class LabResults(Base):
    __tablename__ = 'lab_results'

    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('students.id'))
    laba_id = db.Column(db.Integer, db.ForeignKey('labs.id'))

    admission_score = db.Column(db.Integer)
    visiting = db.Column(db.Boolean)
    practice_score = db.Column(db.Integer)
    report = db.Column(db.Boolean)
    report_score = db.Column(db.Integer)

    student = relationship("Student", back_populates="labs")
    laba = relationship("Laba")


    def __init__(self, **kwargs):
            self.student_id = kwargs.get('student_id')
            self.laba_id = kwargs.get('laba_id')



    def save(self):
        try:
            session.add(self)
            session.commit()
        except Exception:
            session.rollback()
            raise
        

    @property
    def pk(self):
        return self.id


    @property
    def tests_results(self):
        query = session.query(SubmitTest)
        query = query.join(Test, Test.id == SubmitTest.test_id)
        query = query.join(Laba, Laba.id == Test.laba_id)
        query = query.filter(Laba.id == self.laba_id)
        query = query.filter(SubmitTest.student_id == self.student_id)
        
        return query.all()
    

    @property
    def report_link(self):
        if self.report:
            return f"http://www.infochemistryweb.ru/files/user_reports/otchet_{self.id}_{self.student_id}.pdf"
        return None



class Admin(Base):
    __tablename__ = 'admins'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    def __init__(self, **kwargs):
        self.user_id = kwargs.get('user_id')    


    def save(self):
        try:
            session.add(self)
            session.commit()
        except Exception:
            session.rollback()
            raise



class Student(Base):
    __tablename__ = 'students'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(250), nullable=False)
    last_name = db.Column(db.String(250), nullable=False)
    middle_name = db.Column(db.String(250), nullable=False)
    email = db.Column(db.String(250), nullable=False, unique=True)
    password = db.Column(db.String(250), nullable=False)
    isu_number = db.Column(db.String(250), nullable=False, unique=True)
    phone_number = db.Column(db.String(250), nullable=False, unique=True)
    vk_link = db.Column(db.String(255), nullable=True)
    tg_link = db.Column(db.String(255), nullable=True)
    acc_image = db.Column(db.String(255), nullable=True)
    date_reg = db.Column(db.DateTime(), default=datetime.utcnow)

    school = db.Column(db.String(250), nullable=True)
    class_school = db.Column(db.String(250), nullable=True)
    city = db.Column(db.String(250), nullable=True)

    

    groups = relationship("Group", secondary=user_group_association, back_populates="users")
    groups_create = relationship("Group", back_populates="creator")
    submit_tests = relationship("SubmitTest", back_populates="student")
    labs = relationship("LabResults", back_populates="student")


    def __init__(self, **kwargs):
        self.email = kwargs.get('email')
        self.password = bcrypt.hash(kwargs.get('password'))
        self.first_name = kwargs.get('first_name')
        self.last_name = kwargs.get('last_name')
        self.middle_name = kwargs.get('middle_name')
        self.isu_number = kwargs.get('isu_number')
        self.phone_number = kwargs.get('phone_number')


    @property
    def is_admin(self):
        return bool(Admin.query.filter(Admin.user_id == self.id).all())
    
    @property
    def pk(self):
        return self.id

    def get_access_token(self, expire_time_hours=1):
        expire_delta = timedelta(hours=expire_time_hours)
        access_token = create_access_token(
            identity=self.id, expires_delta=expire_delta, fresh=True)
        
        return access_token
    


    def get_refresh_token(self, expire_time_hours=24*30):
        expire_delta = timedelta(hours=expire_time_hours)
        refresh_token = create_refresh_token(
            identity=self.id, expires_delta=expire_delta)
        return refresh_token

    
    def update_admin(self, value):
        if value:
            if self.is_admin:
                return
            Admin(user_id=self.id).save()
        else:
            if not self.is_admin:
                return
            session.delete(Admin.query.get(self.id))
            session.commit()
            

    def save(self):
        try:
            session.add(self)
            session.commit()
        except Exception:
            session.rollback()
            raise


    @classmethod
    def authenticate(cls, email, password):
        student = cls.query.filter(cls.email == email).one()
        if not bcrypt.verify(password, student.password):
            raise Exception('No user with this password')
        return student

    @classmethod
    def get_user_for_id(cls, user_id):
        student = cls.query.filter(cls.id == user_id).one()
        return student
