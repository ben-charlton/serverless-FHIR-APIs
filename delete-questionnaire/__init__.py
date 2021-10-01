import logging
from models.api import delete_questionnaire
import azure.functions as func
from models.api import verify_user

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    user_id = req.headers.get('authorisation')
    if not verify_user(user_id):
        return func.HttpResponse(status_code=401)

    res = delete_questionnaire(req.route_params.get('uid'), user_id)

    if (res==True):
        return func.HttpResponse(body="successfully deleted resource", status_code=200)
    else:
       return func.HttpResponse(body=str(res), status_code=500)
    
    
    