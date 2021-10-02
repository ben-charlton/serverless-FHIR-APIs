import logging
import azure.functions as func
import pyodbc
import json
import urllib
import sqlalchemy 
from models.api import post_questionnaire
from models.api import verify_user

#AuthenticationHeaderValue("Bearer", Request.Headers["X-MS-TOKEN-AAD-ACCESS-TOKEN"]);


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    user_id = req.headers.get('authorisation')
    if not verify_user(user_id):
        return func.HttpResponse(status_code=401)

    res = None
    try:
        res = post_questionnaire(req.get_json(), user_id)
    except Exception as e:
        error = "Error: " + str(e)

    if res:
        return func.HttpResponse(body=res, status_code=200)
    else:
        return func.HttpResponse(body=error, status_code=500)
    

