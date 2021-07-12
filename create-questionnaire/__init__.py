import logging
import azure.functions as func
import pyodbc
import requests 
import json
import urllib
import sqlalchemy 
from models.questionnaire import Questionnaire


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    json_dict = req.get_json()
    created_questionnaire = Questionnaire()
    created_questionnaire.update_with_json(json_dict)
    did_save = created_questionnaire.save()

    if did_save:
        return func.HttpResponse(body="success", status_code=200)
    else:
        return func.HttpResponse(body="failed", status_code=500)
    

