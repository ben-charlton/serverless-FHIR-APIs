import logging
import json
import azure.functions as func
import os
from models.api import get_questionnaire


def main(req: func.HttpRequest) -> func.HttpResponse:

    user_id = req.headers.get('authorisation')

    
    data = None
    query = req.route_params
    logging.info(f'query is {query}')
    if len(query.keys()) != 1 and 'uid' not in query.keys():
        return func.HttpResponse(body="Error: Invalid Query", status_code=500)
    else:
        try:
            data = get_questionnaire(req.route_params, user_id)
        except Exception as e:
            error = "Error: " + str(e)
            return func.HttpResponse(body=error, status_code=500)
        return func.HttpResponse(body=data, headers={"content-type": "application/json"}, status_code=200)

        

   

