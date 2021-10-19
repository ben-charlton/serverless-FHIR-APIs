import logging
from models.api import get_questionnaireResponse
import azure.functions as func


def main(req: func.HttpRequest) -> func.HttpResponse:
    
    data = None 
    query = req.route_params

    try: 
        user_id = req.headers.get('authorisation')
    except:
        return func.HttpResponse(body="Invalid authorisation supplied", status_code=400)

    
    if len(query.keys()) != 1 and 'uid' not in query.keys():
        return func.HttpResponse(body="Error: Invalid Query", status_code=400)
    else:
        try:
            data = get_questionnaireResponse(req.route_params, user_id)
            return func.HttpResponse(body=data, headers={"content-type": "application/json"}, status_code=200)
        except Exception as e:
            error = "Error: " + str(e)
            if (error == "Error: No row was found when one was required"):
                return func.HttpResponse(status_code=204)
            return func.HttpResponse(body=error, status_code=400)
    return func.HttpResponse(body="error", status_code=500)

