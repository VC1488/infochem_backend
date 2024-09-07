from marshmallow import Schema, validate, fields, ValidationError


class MessageSchema(Schema):
    message = fields.String(dump_only=True)


class VideoSchema(Schema):
    id = fields.Integer(dump_only=True)
    user_id = fields.Integer(dump_only=True)
    name = fields.String(required=True, validate=[
        validate.Length(max=250)])
    description = fields.String(required=True, validate=[
        validate.Length(max=500)])
    message = fields.String(dump_only=True)



class LoginRequest(Schema):
    email = fields.String(required=True, validate=[
        validate.Email(error="Invalid email.")])
    password = fields.String(required=True, validate=[
        validate.Length(max=250)])

class CustomRegisterRequest(Schema):
    first_name = fields.String(required=True, validate=[
        validate.Length(max=250)])
    last_name = fields.String(required=True, validate=[
        validate.Length(max=250)])
    middle_name = fields.String(required=True, validate=[
        validate.Length(max=250)])
    email = fields.String(required=True, validate=[
        validate.Email(error="Invalid email.")])
    password1 = fields.String(required=True, validate=[
        validate.Length(max=250)])
    password2 = fields.String(required=True, validate=[
        validate.Length(max=250)])
    isu_number = fields.Integer(required=True)
    phone_number = fields.String(required=True, validate=[
        validate.Length(max=250)])
    

class CustomStudentDetailsSchema(Schema):
    pk = fields.Integer(dump_only=True)
    first_name = fields.String(dump_only=True, validate=[
        validate.Length(max=250)])
    last_name = fields.String(dump_only=True, validate=[
        validate.Length(max=250)])
    middle_name = fields.String(dump_only=True, validate=[
        validate.Length(max=250)])
    email = fields.String(dump_only=True, validate=[
        validate.Email(error="Invalid email.")])
    isu_number = fields.String(dump_only=True, validate=[
        validate.Length(max=250)])
    phone_number = fields.String(dump_only=True, validate=[
        validate.Length(max=250)])
    vk_link = fields.String(dump_only=True, validate=[
        validate.Length(max=255)])
    tg_link = fields.String(dump_only=True, validate=[
        validate.Length(max=255)])
    acc_image = fields.String(dump_only=True, validate=[
        validate.Length(max=255)])
    is_admin = fields.Boolean(dump_only=True)
    city = fields.String(dump_only=True, validate=[
        validate.Length(max=255)])
    class_school = fields.String(dump_only=True, validate=[
        validate.Length(max=255)])
    school = fields.String(dump_only=True, validate=[
        validate.Length(max=255)])
    

class CustomStudentFIOSchema(Schema):
    pk = fields.Integer(dump_only=True)
    first_name = fields.String(dump_only=True, validate=[
        validate.Length(max=250)])
    last_name = fields.String(dump_only=True, validate=[
        validate.Length(max=250)])
    middle_name = fields.String(dump_only=True, validate=[
        validate.Length(max=250)])
    

class PatchedCustomUserDetailsRequest(Schema):
    phone_number = fields.String(validate=[
        validate.Length(max=250)])
    email = fields.String( validate=[
        validate.Email(error="Invalid email.")])
    tg_link = fields.String( validate=[
        validate.Length(max=255)])
    vk_link = fields.String(validate=[
        validate.Length(max=255)])
    acc_image = fields.String(validate=[
        validate.Length(max=255)])
    city = fields.String(validate=[
        validate.Length(max=255)])
    class_school = fields.String(validate=[
        validate.Length(max=255)])
    school = fields.String(validate=[
        validate.Length(max=255)])
    
    

class JWTSchema(Schema):
    access_token = fields.String(dump_only=True)
    refresh_token = fields.String(dump_only=True)
    user = fields.Nested(CustomStudentDetailsSchema, dump_only=True)





class StudentsResponse(Schema):
    students = fields.List(fields.Nested(CustomStudentDetailsSchema, dump_only=True))



class AdminPatchedCustomStudentDetailsRequest(Schema):
    phone_number = fields.String(validate=[
        validate.Length(max=250)])
    email = fields.String( validate=[
        validate.Email(error="Invalid email.")])
    tg_link = fields.String( validate=[
        validate.Length(max=255)])
    vk_link = fields.String(validate=[
        validate.Length(max=255)])
    acc_image = fields.String(validate=[
        validate.Length(max=255)])
    is_admin = fields.Boolean()
    city = fields.String(validate=[
        validate.Length(max=255)])
    class_school = fields.String(validate=[
        validate.Length(max=255)])
    school = fields.String(validate=[
        validate.Length(max=255)])
    


class TokenRefresh(Schema):
    access_token = fields.String(dump_only=True)


class CustomGroupSchema(Schema):
    pk = fields.Integer(dump_only=True)
    name = fields.String(dump_only=True, validate=[
        validate.Length(max=250)])
    students = fields.List(fields.Nested(CustomStudentDetailsSchema, dump_only=True))
    

class CustomGroupSchemaSimple(Schema):
    pk = fields.Integer(dump_only=True)
    name = fields.String(dump_only=True, validate=[
        validate.Length(max=250)])


class GroupsResponse(Schema):
    groups = fields.List(fields.Nested(CustomGroupSchema, dump_only=True))



class NewGroupRequest(Schema):
    name = fields.String(validate=[
        validate.Length(max=255)])
    students = fields.List(
        fields.Integer(),
        required=True
    )

class AdminPatchedCustoGroupDetailsRequest(Schema):
    students = fields.List(
        fields.Integer()
    )
    labs = fields.List(
        fields.Integer()
    )
    name = fields.String(validate=[
        validate.Length(max=250)])
    creator_id = fields.Integer()
        

# sectionlabs
class CustomSectionsLabaSchema(Schema):
    pk = fields.Integer(dump_only=True)
    name = fields.String(validate=[
        validate.Length(max=250)])

class AllSectionsLabaSchema(Schema):
    sections = fields.List(fields.Nested(CustomSectionsLabaSchema, dump_only=True))




# labs

class CustomLabaSchema(Schema):
    pk = fields.Integer(dump_only=True)
    name = fields.String(dump_only=True, validate=[
        validate.Length(max=250)])
    link = fields.String(dump_only=True, validate=[
        validate.Length(max=250)])
    is_active = fields.Boolean(dump_only=True)
    groups = fields.List(fields.Nested(CustomGroupSchemaSimple, dump_only=True))
    section = fields.Nested(CustomSectionsLabaSchema, dump_only=True)


class CustomLabaSimpleSchema(Schema):
    pk = fields.Integer(dump_only=True)
    name = fields.String(dump_only=True, validate=[
        validate.Length(max=250)])




class UploadLabaRequest(Schema):
    pk = fields.Integer()

    

class LabsResponse(Schema):
    labs = fields.List(fields.Nested(CustomLabaSchema, dump_only=True))


class NewLabaRequest(Schema):
    name = fields.String( validate=[
        validate.Length(max=255)])
    section_id = fields.Integer()


class AdminPatchedCustomLabaDetailsRequest(Schema):
    groups = fields.List(
        fields.Integer()
    )
    name = fields.String(validate=[
        validate.Length(max=250)])
    is_active = fields.Boolean()
    section_id = fields.Integer()


class SectionIdResponse(Schema):
    section_id = fields.Integer()




class TestAnswerDetails(Schema):
    pk = fields.Integer(dump_only=True)
    answer = fields.String(required=True)
    flag = fields.Boolean()


class TestQuestionDetails(Schema):
    pk = fields.Integer(dump_only=True)
    question = fields.String(required=True)
    image = fields.String()
    answers = fields.List(fields.Nested(TestAnswerDetails), validate=validate.Length(min=1), required=True)


class TestSchema(Schema):
    pk = fields.Integer(dump_only=True)
    name = fields.String(required=True)
    laba_id = fields.Integer(required=True)
    attempts = fields.Integer(required=True)
    questions = fields.List(fields.Nested(TestQuestionDetails), validate=validate.Length(min=1), required=True)
    
    
class TestSchemaSimple(Schema):
    pk = fields.Integer(dump_only=True)
    name = fields.String(required=True)
    laba_id = fields.Integer(required=True)
    attempts = fields.Integer(required=True)


class AllTestsSchema(Schema):
    tests = fields.List(fields.Nested(TestSchemaSimple), validate=validate.Length(min=1), required=True)




class AdminPatchedCustomTestDetailsRequest(Schema):
    attempts = fields.Integer()
    name = fields.String()
    questions = fields.List(fields.Nested(TestQuestionDetails), validate=validate.Length(min=1))





class SubmitTestRequestRequest(Schema):
    answers = fields.List(
        fields.Integer(),
        validate=validate.Length(min=1),
        required=True
    )


class SubmitTestResponse(Schema):
    score = fields.Integer(dump_only=True)
    max_score = fields.Integer(dump_only=True)
    date = fields.String(dump_only=True)
    pk_test = fields.Integer(dump_only=True)


class LabResultsSchema(Schema):
    pk = fields.Integer(dump_only=True)
    student = fields.Nested(CustomStudentFIOSchema)
    laba = fields.Nested(CustomLabaSimpleSchema)

    admission_score = fields.Integer()
    visiting = fields.Boolean()
    practice_score = fields.Integer()
    report = fields.Boolean()
    report_link = fields.String(dump_only=True)
    report_score = fields.Integer()

    tests_results = fields.List(
        fields.Nested(SubmitTestResponse), 
        dump_only=True
    )



class GetLabsForUserResponse(Schema):
    labs = fields.List(
        fields.Nested(LabResultsSchema), 
        dump_only=True
    )


class PatchedLabResultsSchema(Schema):
    admission_score = fields.Integer()
    visiting = fields.Boolean()
    practice_score = fields.Integer()
    report_score = fields.Integer()
