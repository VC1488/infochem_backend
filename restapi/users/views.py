from flask import Blueprint, jsonify, request
from restapi import logger, session, docs
from restapi.schemas import *
from flask_apispec import use_kwargs, marshal_with, doc
from restapi.models import Student, SectionLaba, Group, Laba, Test, TestAnswer, TestQuestion, SubmitTest, LabResults,user_group_association,laba_group_association
from flask_jwt_extended import jwt_required, get_jwt_identity
import traceback, os
from sqlalchemy import and_


users = Blueprint('users', __name__)

@doc(tags=['labs'])
@users.route('/labs/<int:laba_id>', methods=['PATCH'])
@jwt_required(fresh=True)
@marshal_with(CustomLabaSchema, code=200)
@marshal_with(MessageSchema)
@use_kwargs(AdminPatchedCustomLabaDetailsRequest)
def patch_laba(laba_id, **kwargs):
    try:
        user_id = get_jwt_identity()
        user = Student.query.get(user_id)
        if not user.is_admin:
            return {'message': 'Not admin'}, 400
        laba = Laba.query.get(laba_id)
        if not laba:
            return {'message': 'Not laba'}, 400
        for key, value in kwargs.items():
            if key == "groups":
                laba.groups = []
                for group_id in value:
                    group = Group.query.filter(and_(Group.id == group_id, Group.creator_id == user_id)).first()
                    if group:
                        laba.groups.append(group)
                continue
            setattr(laba, key, value)
        print(kwargs.items())
        laba.save()

        return laba
    except Exception as e:
        logger.warning(
            f'registration failed with errors: {e}')
        return {'message': str(e)}, 400




@doc(tags=['labs'])
@users.route('/labs/<int:laba_id>', methods=['DELETE'])
@jwt_required(fresh=True)
@marshal_with(MessageSchema)
def delete_laba(laba_id, **kwargs):
    try:
        user_id = get_jwt_identity()
        user = Student.query.get(user_id)
        if not user.is_admin:
            return {'message': 'Not admin'}, 400
        laba = Laba.query.get(laba_id)
        if not laba:
            return {'message': 'Not laba'}, 400
        session.delete(laba)
        session.commit()
        return {'message': "OK"}
    except Exception as e:
        logger.warning(
            f'registration failed with errors: {e}')
        return {'message': str(e)}, 400
    


@doc(tags=['labs'])
@users.route('/labs/<int:laba_id>', methods=['GET'])
@jwt_required(fresh=True)
@marshal_with(CustomLabaSchema, code=200)
@marshal_with(MessageSchema)
def get_laba(laba_id, **kwargs):
    try:
        user_id = get_jwt_identity()
        user = Student.query.get(user_id)
        if not user.is_admin:
            return {'message': 'Not admin'}, 400
        laba = Laba.query.get(laba_id)
        if not laba:
            return {'message': 'Not laba'}, 400
        return laba
    except Exception as e:
        logger.warning(
            f'registration failed with errors: {e}')
        return {'message': str(e)}, 400



@doc(tags=['labs'])
@users.route('/labs/new', methods=['POST'])
@jwt_required(fresh=True)
@use_kwargs(NewLabaRequest)
@marshal_with(CustomLabaSchema, code=200)
@marshal_with(MessageSchema)
def new_laba(**kwargs):
    try:
        user_id = get_jwt_identity()
        user = Student.query.get(user_id)
        if not user.is_admin:
            return {'message': 'Not admin'}, 400
        
        laba = Laba(**kwargs)
        laba.save()
        return laba
    except Exception as e:
        logger.warning(
            f'registration failed with errors: {e}')
        return {'message': str(e)}, 400


@doc(tags=['labs'])
@users.route('/labs', methods=['GET'])
@jwt_required(fresh=True)
@marshal_with(LabsResponse, code=200)
@marshal_with(MessageSchema)
@use_kwargs(SectionIdResponse, location="query")
def get_labs(section_id=None):
    try:
        if section_id:
            return {"labs": Laba.query.filter(Laba.section_id == section_id).all()}
        return {"labs": Laba.query.all()}

    except Exception as e:
        logger.warning(
            f'registration failed with errors: {e}')
        return {'message': str(e)}, 400




@doc(tags=['labs'])
@users.route('/labs/<int:laba_id>/upload', methods=['POST'])
@jwt_required(fresh=True)
@marshal_with(CustomLabaSchema, code=200)
@marshal_with(MessageSchema)
def upload_pdf_to_laba(laba_id, **kwargs):
    try:
        user_id = get_jwt_identity()
        user = Student.query.get(user_id)
        if not user.is_admin:
            return {'message': 'Not admin'}, 400
        laba = Laba.query.get(laba_id)
        if not laba:
            return {'message': 'Not laba'}, 400
        
        if 'file' not in request.files:
            return {'message': 'No file part in the request'}, 400
        file = request.files['file']

        if file.filename == '':
            return {'message': 'No selected file'}, 400
        if file:
            file.save(os.path.join("/home/files", f"{laba.id}.pdf"))
        else:
            return {'message': 'Invalid file type'}, 400
        return laba
    except Exception as e:
        logger.warning(
            f'registration failed with errors: {e}')
        return {'message': str(e)}, 400






@doc(tags=['Auth'])
@users.route('/auth/token/refresh', methods=['POST'])
@marshal_with(JWTSchema, code=200)
@marshal_with(MessageSchema)
@jwt_required(refresh=True)
def refresh(**kwargs):
    user_id = get_jwt_identity()
    user = Student.query.get(user_id)
    access_token = user.get_access_token()
    return {"access_token": access_token}




@doc(tags=['Auth'])
@users.route('/auth/register', methods=['POST'])
@use_kwargs(CustomRegisterRequest)
@marshal_with(JWTSchema, code=200)
@marshal_with(MessageSchema)
def register(**kwargs):
    try:
        user = Student(
            first_name=kwargs["first_name"],
            last_name=kwargs["last_name"], 
            middle_name=kwargs["middle_name"], 
            email=kwargs["email"], 
            isu_number=kwargs["isu_number"], 
            phone_number=kwargs["phone_number"], 
            password=kwargs["password1"])
        user.save()

        access_token = user.get_access_token()
        refresh_token = user.get_refresh_token()
    except Exception as e:
        logger.warning(
            f'registration failed with errors: {e}')
        return {'message': str(e)}, 400
    return {'access_token': access_token, "refresh_token": refresh_token, "user": user}



@doc(tags=['Auth'])
@users.route('/auth/login', methods=['POST'])
@use_kwargs(LoginRequest)
@marshal_with(JWTSchema, code=200)
@marshal_with(MessageSchema)
def login(**kwargs):

    try:
        user = Student.authenticate(**kwargs)
        access_token = user.get_access_token()
        refresh_token = user.get_refresh_token()
    except Exception as e:
        logger.warning(
            f'login with email {kwargs["email"]} failed with errors: {e}')
        return {'message': str(e)}, 400
    return {'access_token': access_token, "refresh_token": refresh_token, "user": user}


@doc(tags=['Auth'])
@users.route('/auth/user', methods=['GET'])
@marshal_with(CustomStudentDetailsSchema, code=200)
@marshal_with(MessageSchema)
@jwt_required(fresh=True)
def get_user_req(**kwargs):
    try:
        user_id = get_jwt_identity()
        user = Student.query.get(user_id)

    except Exception as e:
        logger.warning(
            f'errors: {e}')
        return {'message': str(e)}, 400
    return user



@doc(tags=['Auth'])
@users.route('/auth/user', methods=['PUT', 'PATCH'])
@jwt_required(fresh=True)
@marshal_with(CustomStudentDetailsSchema, code=200)
@marshal_with(MessageSchema)
@use_kwargs(PatchedCustomUserDetailsRequest)
def update_user(**kwargs):
    try:
        user_id = get_jwt_identity()
        user = Student.query.get(user_id)
        for key, value in kwargs.items():
            setattr(user, key, value)
        user.save()
        
    except Exception as e:
        logger.warning(
            f'errors: {e}')
        return {'message': str(e)}, 400
    return user



@doc(tags=['Students'])
@users.route('/students', methods=['GET'])
@marshal_with(StudentsResponse, code=200)
@marshal_with(MessageSchema)
@jwt_required(fresh=True)
def get_students():
    try:
        user_id = get_jwt_identity()
        user = Student.query.get(user_id)
        if user.is_admin:
            return {"students": Student.query.all()}
        return {'message': 'Not admin'}, 400

    except Exception as e:
        logger.warning(
            f'errors: {e}')
        return {'message': str(e)}, 400
    

@doc(tags=['Students'])
@users.route('/students/<int:student_id>', methods=['GET'])
@jwt_required(fresh=True)
@marshal_with(CustomStudentDetailsSchema, code=200)
@marshal_with(MessageSchema)
def get_student(student_id, **kwargs):
    try:
        user_id = get_jwt_identity()
        user = Student.query.get(user_id)
        if not user.is_admin:
            return {'message': 'Not admin'}, 400
        student = Student.query.get(student_id)
        return student
        
    except Exception as e:
        logger.warning(
            f'errors: {e}')
        return {'message': str(e)}, 400
    

@doc(tags=['Students'])
@users.route('/students/<int:student_id>', methods=['PUT', 'PATCH'])
@jwt_required(fresh=True)
@marshal_with(CustomStudentDetailsSchema, code=200)
@marshal_with(MessageSchema)
@use_kwargs(AdminPatchedCustomStudentDetailsRequest)
def update_student_adm(student_id, **kwargs):
    try:
        user_id = get_jwt_identity()
        user = Student.query.get(user_id)
        if not user.is_admin:
            return {'message': 'Not admin'}, 400
        student = Student.query.get(student_id)
        for key, value in kwargs.items():
            if key == "is_admin":
                student.update_admin(value)
                continue
            setattr(student, key, value)
        student.save()
        
    except Exception as e:
        logger.warning(
            f'errors: {e}')
        return {'message': str(e)}, 400
    return student


# groups
@doc(tags=['Groups'])
@users.route('/groups/new', methods=['POST'])
@jwt_required(fresh=True)
@use_kwargs(NewGroupRequest)
@marshal_with(CustomGroupSchema, code=200)
@marshal_with(MessageSchema)
def new_group(**kwargs):
    try:
        user_id = get_jwt_identity()
        user = Student.query.get(user_id)
        if not user.is_admin:
            return {'message': 'Not admin'}, 400
        group = Group(name=kwargs["name"], creator_id=user_id)
        group.save()
        for i in kwargs["students"]:
            student = Student.query.get(i)
            if student:
                group.users.append(student)
        group.save()
    except Exception as e:
        logger.warning(
            f'registration failed with errors: {e}')
        return {'message': str(e)}, 400
    return group



@doc(tags=['Groups'])
@users.route('/groups/<int:group_id>', methods=['GET'])
@jwt_required(fresh=True)
@marshal_with(CustomGroupSchema, code=200)
@marshal_with(MessageSchema)
def get_group_for_id(group_id, **kwargs):
    try:
        user_id = get_jwt_identity()
        user = Student.query.get(user_id)
        if not user.is_admin:
            return {'message': 'Not admin'}, 400
        group = Group.query.filter(and_(Group.id == group_id, Group.creator_id == user_id)).all()
        if not group:
            return {'message': 'Not group'}, 400
        group = group[0]
    except Exception as e:
        logger.warning(
            f'registration failed with errors: {e}')
        return {'message': str(e)}, 400
    return {"pk": group.pk, "name": group.name, "students": group.users}






@doc(tags=['Groups'])
@users.route('/groups/<int:group_id>', methods=['PATCH'])
@jwt_required(fresh=True)
@marshal_with(CustomGroupSchema, code=200)
@marshal_with(MessageSchema)
@use_kwargs(AdminPatchedCustoGroupDetailsRequest)
def patch_group(group_id, **kwargs):
    try:
        user_id = get_jwt_identity()
        user = Student.query.get(user_id)
        if not user.is_admin:
            return {'message': 'Not admin'}, 400
        group = Group.query.filter(and_(Group.id == group_id, Group.creator_id == user_id)).first()
        if not group:
            return {'message': 'Not group'}, 400
        for key, value in kwargs.items():
            if key == "students":
                group.users = []
                for student_id in value:
                    student = Student.query.get(student_id)
                    if student and student not in group.users:
                        group.users.append(student)
                continue
            if key == "labs":
                group.labs = []
                for laba_id in value:
                    laba = Laba.query.get(laba_id)
                    if laba and laba not in group.labs:
                        group.labs.append(laba)
                continue
            setattr(group, key, value)
        group.save()

        return group
    except Exception as e:
        logger.warning(
            f'registration failed with errors: {e}')
        return {'message': str(e)}, 400




@doc(tags=['Groups'])
@users.route('/groups', methods=['GET'])
@jwt_required(fresh=True)
@marshal_with(GroupsResponse, code=200)
@marshal_with(MessageSchema)
def get_groups(**kwargs):
    try:
        user_id = get_jwt_identity()
        user = Student.query.get(user_id)
        if not user.is_admin:
            return {'message': 'Not admin'}, 400
        groups = user.groups_create
    except Exception as e:
        logger.warning(
            f'registration failed with errors: {e}')
        return {'message': str(e)}, 400
    return {"groups": [{"pk": i.pk, "name": i.name} for i in groups]}









@doc(tags=['SectionsLabs'])
@users.route('/sections_labs', methods=['GET'])
@jwt_required(fresh=True)
@marshal_with(AllSectionsLabaSchema, code=200)
@marshal_with(MessageSchema)
def get_sections_labs(**kwargs):
    try:
        user_id = get_jwt_identity()
        user = Student.query.get(user_id)
        if not user.is_admin:
            return {'message': 'Not admin'}, 400
    except Exception as e:
        logger.warning(
            f'registration failed with errors: {e}')
        return {'message': str(e)}, 400
    return {"sections": SectionLaba.query.all()}
    

@doc(tags=['SectionsLabs'])
@users.route('/sections_labs/new', methods=['POST'])
@jwt_required(fresh=True)
@marshal_with(CustomSectionsLabaSchema, code=200)
@marshal_with(MessageSchema)
@use_kwargs(CustomSectionsLabaSchema)
def new_section_laba(**kwargs):
    try:
        user_id = get_jwt_identity()
        user = Student.query.get(user_id)
        if not user.is_admin:
            return {'message': 'Not admin'}, 400
        section = SectionLaba(name=kwargs["name"])
        section.save()
    except Exception as e:
        logger.warning(
            f'registration failed with errors: {e}')
        return {'message': str(e)}, 400
    return section
    


@doc(tags=['SectionsLabs'])
@users.route('/sections_labs/<int:section_id>', methods=['GET'])
@jwt_required(fresh=True)
@marshal_with(CustomSectionsLabaSchema, code=200)
@marshal_with(MessageSchema)
def get_section_laba(section_id, **kwargs):
    try:
        user_id = get_jwt_identity()
        user = Student.query.get(user_id)
        if not user.is_admin:
            return {'message': 'Not admin'}, 400
        section = SectionLaba.query.get(section_id)
        if not section:
            return {'message': 'Not section'}, 400
    except Exception as e:
        logger.warning(
            f'registration failed with errors: {e}')
        return {'message': str(e)}, 400
    return section
    

@doc(tags=['SectionsLabs'])
@users.route('/sections_labs/<int:section_id>', methods=['PATCH'])
@jwt_required(fresh=True)
@marshal_with(CustomSectionsLabaSchema, code=200)
@marshal_with(MessageSchema)
@use_kwargs(CustomSectionsLabaSchema)
def patch_section_laba(section_id, **kwargs):
    try:
        user_id = get_jwt_identity()
        user = Student.query.get(user_id)
        if not user.is_admin:
            return {'message': 'Not admin'}, 400
        section = SectionLaba.query.get(section_id)
        if not section:
            return {'message': 'Not section'}, 400
        

        for key, value in kwargs.items():
            setattr(section, key, value)
        section.save()
    except Exception as e:
        logger.warning(
            f'registration failed with errors: {e}')
        return {'message': str(e)}, 400
    return section





@doc(tags=['Test'])
@users.route('/tests/new', methods=['POST'])
@jwt_required(fresh=True)
@marshal_with(TestSchema, code=200)
@marshal_with(MessageSchema)
@use_kwargs(TestSchema)
def new_test(**kwargs):
    try:
        user_id = get_jwt_identity()
        user = Student.query.get(user_id)
        if not user.is_admin:
            return {'message': 'Not admin'}, 400
        
        test = Test(name=kwargs["name"], laba_id=kwargs["laba_id"], attempts=kwargs["attempts"])
        test.save()
        for i in kwargs["questions"]:
            question = TestQuestion(
                test_id=test.id, 
                question=i["question"],
                image=i.get("image"))
            question.save()
            for j in i["answers"]:
                TestAnswer(
                    question_id=question.id,
                    answer=j["answer"],
                    flag=j.get("flag")
                ).save()

                
    except Exception as e:
        logger.warning(
            f'registration failed with errors: {e}')
        return {'message': str(e)}, 400
    return test


@doc(tags=['Test'])
@users.route('/tests', methods=['GET'])
@jwt_required(fresh=True)
@marshal_with(AllTestsSchema, code=200)
@marshal_with(MessageSchema)
def get_tests(**kwargs):
    try:
        user_id = get_jwt_identity()
        user = Student.query.get(user_id)
    except Exception as e:
        logger.warning(
            f'registration failed with errors: {e}')
        return {'message': str(e)}, 400
    return  {"tests": Test.query.all()}



@doc(tags=['Test'])
@users.route('/tests/<int:test_id>', methods=['GET'])
@jwt_required(fresh=True)
@marshal_with(TestSchema, code=200)
@marshal_with(MessageSchema)
def get_test(test_id, **kwargs):
    try:
        user_id = get_jwt_identity()
        user = Student.query.get(user_id)
        test = Test.query.get(test_id)
        if not test:
            return {'message': 'Not test'}, 400


    except Exception as e:
        logger.warning(
            f'registration failed with errors: {e}')
        return {'message': str(e)}, 400
    return test



@doc(tags=['Test'])
@users.route('/tests/<int:test_id>', methods=['PATCH'])
@jwt_required(fresh=True)
@marshal_with(TestSchema, code=200)
@marshal_with(MessageSchema)
@use_kwargs(AdminPatchedCustomTestDetailsRequest)
def patch_test(test_id, **kwargs):
    try:
        user_id = get_jwt_identity()
        user = Student.query.get(user_id)
        if not user.is_admin:
            return {'message': 'Not admin'}, 400
        
        test = Test.query.get(test_id)
        if not test:
            return {'message': 'Not test'}, 400
        

        for key, value in kwargs.items():
            if key == "questions":
                TestAnswer.query.filter(TestAnswer.question_id.in_([q.id for q in test.questions])).delete()
                TestQuestion.query.filter_by(test_id=test.id).delete()
                session.commit()
                for i in kwargs["questions"]:
                    question = TestQuestion(
                        test_id=test.id, 
                        question=i["question"],
                        image=i.get("image"))
                    question.save()
                    for j in i["answers"]:
                        TestAnswer(
                            question_id=question.id,
                            answer=j["answer"],
                            flag=j.get("flag")
                        ).save()
                continue
            setattr(test, key, value)
        
        
        test.save()

    except Exception as e:
        logger.warning(
            f'registration failed with errors: {e}')
        return {'message': str(e)}, 400
    return test





@doc(tags=['test'])
@users.route('/jwttest', methods=['GET'])
def testreq(**kwargs):
    return jsonify({"status": "ok"})






@doc(tags=['Test'])
@users.route('/tests/<int:test_id>/submit', methods=['POST'])
@jwt_required(fresh=True)
@marshal_with(SubmitTestResponse, code=200)
@marshal_with(MessageSchema)
@use_kwargs(SubmitTestRequestRequest)
def new_submit_test(test_id, **kwargs):
    try:
        user_id = get_jwt_identity()
        user = Student.query.get(user_id)
        test = Test.query.get(test_id)
        if not test:
            return {'message': 'Not test'}, 400
        
        answers = kwargs["answers"]

        score = 0
        max_score = 0

        true_answers = [[j.id for j in i.answers if j.flag] for i in test.questions]
        true_answers = sum(true_answers, [])

        score = len([i for i in answers if i in true_answers])
        max_score = len(true_answers)


        submit = SubmitTest(test_id=test.id, 
                            student_id=user_id,
                            score=score,
                            max_score=max_score)
        submit.save()


    except Exception as e:
        logger.warning(
            f'registration failed with errors: {e}')
        return {'message': str(e)}, 400
    return submit




@doc(tags=['Students'])
@users.route('/students/<int:student_id>/labs/<int:laba_id>/upload', methods=['POST'])
@jwt_required(fresh=True)
@marshal_with(LabResultsSchema, code=200)
@marshal_with(MessageSchema)
def upload_laba_result(student_id, laba_id, **kwargs):
    try:
        user_id = get_jwt_identity()
        user = Student.query.get(user_id)

        is_laba = session.query(laba_group_association).\
        join(Group).\
        join(user_group_association).\
        filter(user_group_association.c.user_id == student_id).\
        filter(laba_group_association.c.laba_id == laba_id).\
        count()


        if is_laba == 0:
            return {"message": "Отказано в доступе"}, 400
        if student_id != user_id and not user.is_admin:
            return {"message": "Отказано в доступе"}, 400
        laba = LabResults.query.filter(and_(LabResults.student_id == user_id, LabResults.laba_id == laba_id)).first()
        if not laba:
            laba = LabResults(student_id = user_id, laba_id = laba_id)
            laba.save()
        
        if 'file' not in request.files:
            return {'message': 'No file part in the request'}, 400
        file = request.files['file']

        if file.filename == '':
            return {'message': 'No selected file'}, 400
        if file:
            file.save(os.path.join("/home/files/user_reports", f"otchet_{laba.id}_{laba.student_id}.pdf"))
        else:
            return {'message': 'Invalid file type'}, 400
        laba.report = True
        laba.save()
        return laba
    except Exception as e:
        logger.warning(
            f'errors: {e}')
        return {'message': str(e)}, 400
    



@doc(tags=['Students'])
@users.route('/students/<int:student_id>/labs/<int:laba_id>', methods=['PATCH'])
@jwt_required(fresh=True)
@marshal_with(LabResultsSchema, code=200)
@marshal_with(MessageSchema)
@use_kwargs(PatchedLabResultsSchema)
def patch_laba_result(student_id, laba_id, **kwargs):
    try:
        user_id = get_jwt_identity()
        user = Student.query.get(user_id)
        laba = Laba.query.get(laba_id)
        if not laba:
            return {"message": "Not laba"}, 400
        

        is_laba = session.query(laba_group_association).\
        join(Group).\
        join(user_group_association).\
        filter(user_group_association.c.user_id == student_id).\
        filter(laba_group_association.c.laba_id == laba_id).\
        count()
        if is_laba == 0:
            return {"message": "Отказано в доступе"}, 400
        if not user.is_admin:
            return {"message": "Отказано в доступе"}, 400
        laba = LabResults.query.filter(and_(LabResults.student_id == student_id, LabResults.laba_id == laba_id)).first()
        if not laba:
            laba = LabResults(student_id = student_id, laba_id = laba_id)
            laba.save()
        
        for key, value in kwargs.items():
            setattr(laba, key, value)
        laba.save()
        return laba
    except Exception as e:
        logger.warning(
            f'errors: {e}')
        return {'message': str(e)}, 400
    



@doc(tags=['Groups'])
@users.route('/groups/<int:group_id>/labs', methods=['GET'])
@jwt_required(fresh=True)
@marshal_with(GetLabsForUserResponse, code=200)
@marshal_with(MessageSchema)
def get_labresult(group_id, **kwargs):
    try:
        user_id = get_jwt_identity()
        user = Student.query.get(user_id)
        if not user.is_admin:
            return {'message': 'Not admin'}, 400
        group = Group.query.filter(and_(Group.id == group_id, Group.creator_id == user_id)).all()
        labs = []
        if not group:
            return {'message': 'Not group'}, 400
        group = group[0]
        users_ids = [i.id for i in group.users]
        labs_ids = [i.id for i in group.labs]

        for student_id in users_ids:
            for laba_id in labs_ids:
                laba = LabResults.query.filter(and_(LabResults.student_id == student_id, LabResults.laba_id == laba_id)).first()
                if not laba:
                    laba = LabResults(student_id = student_id, laba_id = laba_id)
                    laba.save()
                labs.append(laba)
    except Exception as e:
        logger.warning(
            f'registration failed with errors: {e}')
        return {'message': str(e)}, 400
    return {"labs": labs}


@doc(tags=['Groups'])
@users.route('/students/<int:student_id>/labs', methods=['GET'])
@jwt_required(fresh=True)
@marshal_with(GetLabsForUserResponse, code=200)
@marshal_with(MessageSchema)
def get_labresults(student_id, **kwargs):
    try:
        user_id = get_jwt_identity()
        user = Student.query.get(user_id)
        student = Student.query.get(student_id)
        if not user.is_admin and student_id != user_id:
            return {'message': 'Not admin'}, 400
        result_labs = []
        for group in student.groups:
            for i in group.labs:
                laba = LabResults.query.filter(and_(LabResults.student_id == student_id, LabResults.laba_id == i.id)).first()
                if not laba:
                    laba = LabResults(student_id=student_id, laba_id=i.id)
                    laba.save()
                result_labs.append(laba)
    except Exception as e:
        logger.warning(
            f'registration failed with errors: {e}')
        return {'message': str(e)}, 400
    return {"labs": result_labs}


@users.errorhandler(422)
def handle_error(err):
    headers = err.data.get('headers', None)
    messages = err.data.get('messages', ['Invalid Request.'])
    logger.warning(f'Invalid input params: {messages}')
    if headers:
        return jsonify({'message': messages}), 400, headers
    else:
        return jsonify({'message': messages}), 400


docs.register(register, blueprint='users')
docs.register(refresh, blueprint='users')

docs.register(login, blueprint='users')
docs.register(get_user_req, blueprint='users')
docs.register(testreq, blueprint='users')
docs.register(update_user, blueprint='users')
docs.register(get_students, blueprint='users')
docs.register(get_student, blueprint='users')
docs.register(update_student_adm, blueprint='users')


docs.register(new_group, blueprint='users')
docs.register(get_groups, blueprint='users')
docs.register(get_group_for_id, blueprint='users')
docs.register(patch_group, blueprint='users')


docs.register(new_laba, blueprint='users')
docs.register(patch_laba, blueprint='users')
docs.register(delete_laba, blueprint='users')
docs.register(upload_pdf_to_laba, blueprint='users')
docs.register(get_labs, blueprint='users')
docs.register(get_laba, blueprint='users')



docs.register(get_sections_labs, blueprint='users')
docs.register(new_section_laba, blueprint='users')
docs.register(get_section_laba, blueprint='users')
docs.register(patch_section_laba, blueprint='users')


docs.register(new_test, blueprint='users')
docs.register(get_test, blueprint='users')
docs.register(get_tests, blueprint='users')
docs.register(patch_test, blueprint='users')

docs.register(new_submit_test, blueprint='users')

docs.register(upload_laba_result, blueprint='users')
docs.register(patch_laba_result, blueprint='users')
docs.register(get_labresult, blueprint='users')
docs.register(get_labresults, blueprint='users')














