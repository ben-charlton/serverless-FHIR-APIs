import logging
import azure.functions as func
from models.api import post_questionnaireResponse


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    user_id = req.headers.get('authorisation')


    res = None
    try:
        res = post_questionnaireResponse(req.get_json(), user_id)
    except Exception as e:
        error = "Error: " + str(e)

    if res:
        return func.HttpResponse(body=res, status_code=200)
    else:
        return func.HttpResponse(body=error, status_code=500)
