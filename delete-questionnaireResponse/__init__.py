import logging
from models.api import delete_questionnaireResponse
import azure.functions as func


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    res = delete_questionnaireResponse(req.route_params.get('uid'))

    if (res==True):
        return func.HttpResponse(body="successfully deleted resource", status_code=200)
    else:
       return func.HttpResponse(body=str(res), status_code=500)
