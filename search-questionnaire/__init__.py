import logging
from models.api import get_questionnaire
import azure.functions as func
import json
import logging

def validate_params(params):
    for key in params.keys():
        if key == "name" or key == "title" or key == "id":
            continue
        else:
            return False
    return True


def main(req: func.HttpRequest) -> func.HttpResponse:

    error = None
    data = None

    try: 
        user_id = req.headers.get('authorisation')
    except:
        return func.HttpResponse(body="Invalid authorisation supplied", status_code=400)


    if validate_params(req.params):
        try:
            data = get_questionnaire(req.params, user_id)
        except Exception as e:
            error = "Error: " + str(e)
            if (error == "Error: No row was found when one was required"):
                return func.HttpResponse(status_code=204)
            return func.HttpResponse(body=error, status_code=400)
    return func.HttpResponse(body="Invalid Query Parameters", status_code=400)

