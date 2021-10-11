import logging
from models.api import delete_questionnaire
import azure.functions as func

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    user_id = req.headers.get('authorisation')

    try:
        res = delete_questionnaire(req.route_params.get('uid'), user_id)
    except Exception as e:
        return func.HttpResponse(body=str(e), status_code=500)

    if (res==True):
        return func.HttpResponse(body="successfully deleted resource", status_code=200)
    else:
       return func.HttpResponse(body=str(res), status_code=500)
    
    
    