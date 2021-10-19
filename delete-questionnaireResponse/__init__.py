import logging
from models.api import delete_questionnaireResponse
import azure.functions as func

def main(req: func.HttpRequest) -> func.HttpResponse:

    error = None
    res = None

    try: 
        user_id = req.headers.get('authorisation')
    except:
        return func.HttpResponse(body="Invalid authorisation supplied", status_code=400)

    try:
        res = delete_questionnaire(req.route_params.get('uid'), user_id)
    except Exception as e:
        if (str(e) == 'No resource with matching uid found'):
            return func.HttpResponse(body=str(e), status_code=400)
        elif (str(e) == 'User not found'):
                return func.HttpResponse(body=str(e), status_code=400)
        return func.HttpResponse(body=str(e), status_code=500)

    if (res==True):
        return func.HttpResponse(body="Successfully deleted resource", status_code=200)
    else:
       return func.HttpResponse(body=str(res), status_code=500)
