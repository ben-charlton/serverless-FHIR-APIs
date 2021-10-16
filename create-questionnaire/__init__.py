import logging
import azure.functions as func
import pyodbc
import json
import urllib
import sqlalchemy 
from models.api import post_questionnaire
import time


def main(req: func.HttpRequest) -> func.HttpResponse:
    
    error = None
    res = None

    try: 
        user_id = req.headers.get('authorisation')
    except:
        return func.HttpResponse(body="Invalid authorisation supplied", status_code=400)
    
    try:
        data = req.get_json()
    except:
        return func.HttpResponse(body="Invalid JSON supplied", status_code=400)
    
    try:
        res = post_questionnaire(data, user_id)
    except Exception as e:
        error = "Error: " + str(e)
        return func.HttpResponse(body=error, status_code=400)

    if res:
        return func.HttpResponse(body=res, status_code=200)
    else:
        return func.HttpResponse(body="There was an unidentified error", status_code=500)
    

