import logging
from models.api import delete_questionnaireResponse
import azure.functions as func


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    res = None
    try:
        res = delete_questionnaireResponse(req.route_params)
    except Exception as e:
        error = "Error: " + str(e)

    if res:
        return func.HttpResponse(body="successfully deleted resource", status_code=200)
    else:
        return func.HttpResponse(body=error, status_code=500)
