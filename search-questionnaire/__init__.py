import logging
from models.api import get_questionnaire
import azure.functions as func
import json
import logging
    #if not validate_params(query):
    #    return func.HttpResponse(body="Error: Invalid Query", status_code=500)
    #    else:



def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')
    
    data = None
    try:
        data = get_questionnaire(req.params)
    except Exception as e:
        error = "Error: " + str(e)
        return func.HttpResponse(body=error, status_code=500)
    return func.HttpResponse(body=data, headers={"content-type": "application/json"}, status_code=200)

    

def validate_params(params):
    for key in params.keys():
        print(key)
        logging.info(key)
        if key != "name" or key != "title" or key != "id":
            print('here')
            return False
    return True