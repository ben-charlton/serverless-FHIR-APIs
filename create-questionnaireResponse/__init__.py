import logging
import azure.functions as func
from models.api import post_questionnaireResponse


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    res = post_questionnaireResponse(req.get_json(), path, query)
    if res:
        return func.HttpResponse(body="success", status_code=200)
    else:
        return func.HttpResponse(body="failed", status_code=500)
