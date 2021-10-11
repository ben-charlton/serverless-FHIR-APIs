import logging
import azure.functions as func
from models.api import register_user

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    token = req.headers.get('token')
    if not token:
        return func.HttpResponse(body="Please enter a token as a header value under 'token'", status_code=500)
        
    res = None
    try:
        res = register_user(token)
    except Exception as e:
        error = "Error: " + str(e)

    if res:
        return func.HttpResponse(body=res, status_code=200)
    else:
        return func.HttpResponse(body=error, status_code=500)
    