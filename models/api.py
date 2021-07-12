import json
import requests
import urllib
import logging
from urllib.parse import urljoin

# default type is fhir+json, as the server will only support JSON objects (for now)
FHIRJSONMimeType = 'application/fhir+json'
URIBASE = 'base uri for server here'

def get_questionnaire(path, query):
    headers = {'Accept': 'application/json'}
    return 

def post_questionnaire(path, resource_json):
    url = urljoin(URIBASE, path)
    headers = {
        'Content-type': FHIRJSONMimeType,
        'Accept': FHIRJSONMimeType,
        'Accept-Charset': 'UTF-8',
    }
    return
