import logging
import json
import azure.functions as func
import os
from models.api import get_questionnaire

    # logging.info(f"Headers: {par}")
    # logging.info(f"Params: {req.params}")
    # logging.info(f"Route Params: {req.route_params}")
    # logging.info(f"Body: {req.get_body()}")


    # 1. verify auth token
    #   if not auth
    #       return 403

    #if !authenticate(req):
    #    return 403
    #7a97263ace0b47a882084bfa425a96b2

def main(req: func.HttpRequest) -> func.HttpResponse:
    
    data = None
    query = req.route_params
    logging.info(f'query is {query}')
    if len(query.keys()) != 1 and 'uid' not in query.keys():
        return func.HttpResponse(body="Error: Invalid Query", status_code=500)
    else:
        try:
            data = get_questionnaire(req.route_params)
        except Exception as e:
            error = "Error: " + str(e)
            return func.HttpResponse(body=error, status_code=500)
        return func.HttpResponse(body=data, headers={"content-type": "application/json"}, status_code=200)

        

   

