import logging
import azure.functions as func
from models.api import register_user

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    res = None
    try:
        res = register_user()
    except Exception as e:
        error = "Error: " + str(e)

    if res:
        return func.HttpResponse(body=res, status_code=200)
    else:
        return func.HttpResponse(body=error, status_code=500)
    