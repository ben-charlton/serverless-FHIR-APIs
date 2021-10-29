import logging
from models.api import get_user
import azure.functions as func


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    token = req.headers.get('token')
    if not token:
        return func.HttpResponse(body="Please enter a token as a header value under 'token'", status_code=400)
        
    res = None
    try:
        res = get_user(token)
    except Exception as e:
        error = "Error: " + str(e)
        return func.HttpResponse(body=error, status_code=400)

    if res:
        return func.HttpResponse(body=res, status_code=200)
    else:
        return func.HttpResponse(body=error, status_code=500)
