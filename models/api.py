from models.user import User
from .questionnaireresponse import QuestionnaireResponse
from .questionnaire import Questionnaire


def get_questionnaire(query, user_id):
    retrieved_questionnaire = Questionnaire()
    data = retrieved_questionnaire.load(query, user_id)
    return data

def post_questionnaire(resource_json, user_id):
    created_questionnaire = Questionnaire()
    created_questionnaire.update_with_json(resource_json, user_id)
    res = created_questionnaire.save()
    return res

def get_questionnaireResponse(query, user_id):
    retrieved_response = QuestionnaireResponse()
    data = retrieved_response.load(query, user_id)
    return data

def post_questionnaireResponse(resource_json, user_id):
    created_response = QuestionnaireResponse()
    created_response.update_with_json(resource_json, user_id)
    res = created_response.save()
    return res

def delete_questionnaire(uid, user_id):
    ques_to_delete = Questionnaire()
    res = ques_to_delete.delete(uid, user_id)
    return res

def delete_questionnaireResponse(uid, user_id):
    res_to_delete = QuestionnaireResponse()
    result = res_to_delete.delete(uid, user_id)
    return result

# should take domain name in future
def register_user(token):
    user = User()
    uid = user.save(token)
    return uid

def get_user(token):
    user = User()
    uid = user.load(token)
    return uid

