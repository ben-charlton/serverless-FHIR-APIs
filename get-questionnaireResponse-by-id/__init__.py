import logging
from models.api import get_questionnaireResponse
import azure.functions as func


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    user_id = req.headers.get('authorisation')


    data = None
    query = req.route_params
    if len(query.keys()) != 1 and 'uid' not in query.keys():
        return func.HttpResponse(body="Error: Invalid Query", status_code=500)
    else:
        try:
            data = get_questionnaireResponse(req.route_params, user_id)
        except Exception as e:
            error = "Error: " + str(e)
            return func.HttpResponse(body=error, status_code=500)
        return func.HttpResponse(body=data, headers={"content-type": "application/json"}, status_code=200)

