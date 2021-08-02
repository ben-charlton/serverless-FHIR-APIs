import json
import requests
import urllib
import logging
from urllib.parse import urljoin
from questionnaireresponse import QuestionnaireResponse
from questionnaire import Questionnaire


# default type is fhir+json, as the server will only support JSON objects (for now)
FHIRJSONMimeType = 'application/fhir+json'
URIBASE = 'base uri for server here'


def get_questionnaire(path, query):
    headers = {'Accept': 'application/json'}
    return 

def post_questionnaire(resource_json, path):
    url = urljoin(URIBASE, path)
    headers = {
        'Content-type': FHIRJSONMimeType,
        'Accept': FHIRJSONMimeType,
        'Accept-Charset': 'UTF-8',
    }
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
    res = created_questionnaire.save()
    return res
