import logging
import azure.functions as func
import pyodbc
import requests 
import json
import urllib
import sqlalchemy 
from models.api import post_questionnaire

#AuthenticationHeaderValue("Bearer", Request.Headers["X-MS-TOKEN-AAD-ACCESS-TOKEN"]);


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    res = None
    try:
        res = post_questionnaire(req.get_json())
    except Exception as e:
        error = "Error: " + str(e)

    if res:
        return func.HttpResponse(body=res, status_code=200)
    else:
        return func.HttpResponse(body=error, status_code=500)
    

