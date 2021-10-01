import logging
from models.api import get_questionnaire
import azure.functions as func
import json
import logging
from models.api import verify_user

def validate_params(params):
    for key in params.keys():
        if key == "name" or key == "title" or key == "id":
            continue
        else:
            return False
    return True


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')
    
    user_id = req.headers.get('authorisation')
    if not verify_user(user_id):
        return func.HttpResponse(status_code=401)

    if validate_params(req.params):
        data = None
        try:
            data = get_questionnaire(req.params, user_id)
        except Exception as e:
            error = "Error: " + str(e)
            return func.HttpResponse(body=error, status_code=500)
        return func.HttpResponse(body=data, headers={"content-type": "application/json"}, status_code=200)
    else:
        return func.HttpResponse(body="Error: Invalid Query", status_code=500)
