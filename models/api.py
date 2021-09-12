import json
import urllib
import logging
from urllib.parse import urljoin
from .questionnaireresponse import QuestionnaireResponse
from .questionnaire import Questionnaire

# default type is fhir+json, as the server will only support JSON objects (for now)
FHIRJSONMimeType = 'application/fhir+json'
URIBASE = 'base uri for server here'

#query = {'lat':'45', 'lon':'180'}
#response = requests.get('http://api.open-notify.org/iss-pass.json', params=query)
    # url = urljoin(URIBASE, path)
    # headers = {
    #     'Content-type': FHIRJSONMimeType,
    #     'Accept': FHIRJSONMimeType,
    #     'Accept-Charset': 'UTF-8',
    # }


def get_questionnaire(query):
    retrieved_questionnaire = Questionnaire()
    data = retrieved_questionnaire.load(query)
    return data

def post_questionnaire(resource_json):
    created_questionnaire = Questionnaire()
    created_questionnaire.update_with_json(resource_json)
    res = created_questionnaire.save()
    return res

def get_questionnaireResponse(query):
    retrieved_response = QuestionnaireResponse()
    data = retrieved_response.load(query)
    return data

def post_questionnaireResponse(resource_json):
    created_response = QuestionnaireResponse()
    created_response.update_with_json(resource_json)
    res = created_response.save()
    return res

def delete_questionnaire(uid):
    ques_to_delete = Questionnaire()
    res = ques_to_delete.delete(uid)
    return res

def delete_questionnaireResponse(uid):
    res_to_delete = QuestionnaireResponse()
    result = res_to_delete.delete(uid)
    return result

def authenticate_token(token):
    return True


# f = open('questionnaire.json',)
# data = json.load(f)
# val = post_questionnaireResponse(data)
# print(val)