import json
import requests
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


def get_questionnaire(query):
    retrieved_questionnaire = Questionnaire()
    data = retrieved_questionnaire.load(query)
    return data

def post_questionnaire(resource_json):
    created_questionnaire = Questionnaire()
    created_questionnaire.update_with_json(resource_json)
    res = created_questionnaire.save()
    return res


def get_questionnaireResponse(path, query):
    headers = {'Accept': 'application/json'}
    return 

def post_questionnaireResponse(path, resource_json):
    url = urljoin(URIBASE, path)
    headers = {
        'Content-type': FHIRJSONMimeType,
        'Accept': FHIRJSONMimeType,
        'Accept-Charset': 'UTF-8',
    }
    created_response = Questionnaire()
    created_response.update_with_json(resource_json)
    res = created_response.save()
    return res


# f = open('questionnaire.json',)
# data = json.load(f)
# val = post_questionnaire(data)
# print(val)