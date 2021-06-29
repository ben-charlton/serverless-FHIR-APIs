import logging
import azure.functions as func
import os
import pyodbc
import requests 
import struct
import json

BASE_URL = "https://fhir-questionnaire-api.azurewebsites.net"

# msi_endpoint = os.environ["MSI_ENDPOINT"]
# msi_secret = os.environ["MSI_SECRET"]

# def main(req: func.HttpRequest) -> func.HttpResponse:
#     token_auth_uri = f"{msi_endpoint}?resource=https%3A%2F%2Fdatabase.windows.net%2F&api-version=2017-09-01"
#     head_msi = {'Secret':msi_secret}
#     resp = requests.get(token_auth_uri, headers=head_msi)
#     access_token = resp.json()['access_token']

#     accessToken = bytes(access_token, 'utf-8')
#     exptoken = b""
#     for i in accessToken:
#         exptoken += bytes({i})
#         exptoken += bytes(1)
#     tokenstruct = struct.pack("=i", len(exptoken)) + exptoken

#     conn = pyodbc.connect("Driver={ODBC Driver 17 for SQL Server};Server=tcp:fhir-questionnaire-server.database.windows.net,1433;Database=questionnaire-database", attrs_before = { 1256:bytearray(tokenstruct) })

#     cursor = conn.cursor()
#     cursor.execute("select @@version")
#     row = cursor.fetchall()
#     return func.HttpResponse(str(row))

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    try:
        req_body = req.get_json()
        # get the query parameters from here
        # e.g. like id or whatever?
    except ValueError:
        pass

    db_url = os.environ["CONNECTION_STRING"]

    # then create the questionnaire
    # with a generated id
    # and post it to the database

    return func.HttpResponse(json.dumps(data), headers={"content-type": "application/json"})
