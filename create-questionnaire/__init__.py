import logging
import azure.functions as func
import pyodbc
import requests 
import json
import urllib
import sqlalchemy 
from models.api import post_questionnaire


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')
    res = post_questionnaire(req.get_json(), path, query)
    if res:
        return func.HttpResponse(body="success", status_code=200)
    else:
        return func.HttpResponse(body="failed", status_code=500)
    

