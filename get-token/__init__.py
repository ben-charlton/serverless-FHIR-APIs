import logging
import requests
import azure.functions as func
import json


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    try: 
        client_id = req.get_json().get('client_id')
        client_secret = req.get_json().get('client_secret')
        scope = req.get_json().get('scope')
        grant_type = req.get_json().get('grant_type')
    except Exception as e:
        return func.HttpResponse(body=json.dumps(str(e), indent=4), status_code=400)

    data = {
        "client_id" : client_id,
        "client_secret" : client_secret,
        "scope" : scope,
        "grant_type" : grant_type
    }

    url = "https://login.microsoftonline.com/33e7d565-6558-4ed8-82ba-0882cbafd444/oauth2/v2.0/token"

    r = requests.post(url=url, data=data)
    if r.status_code == 200:
        token = json.dumps(r.json(), indent=4)
        return func.HttpResponse(body=token, status_code=200)
    else:
        return func.HttpResponse(body=r.text, status_code=r.status_code)
