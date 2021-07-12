import json
import requests
import urllib
import logging
from urllib.parse import urljoin

# default type is fhir+json, as the server will only support JSON objects (for now)
FHIRJSONMimeType = 'application/fhir+json'
URIBASE = 'base uri for server here'

def get_json(self, path, nosign=False):
    headers = {'Accept': 'application/json'}
    res = self._get(path, headers, nosign)
    return res.json()

def post_json(self, path, resource_json, nosign=False):
    url = urljoin(self.base_uri, path)
    headers = {
        'Content-type': FHIRJSONMimeType,
        'Accept': FHIRJSONMimeType,
        'Accept-Charset': 'UTF-8',
    }
    if not nosign and self.auth is not None and self.auth.can_sign_headers():
        headers = self.auth.signed_headers(headers)
        
    # perform the request but intercept 401 responses, raising our own Exception
    res = self.session.post(url, headers=headers, data=json.dumps(resource_json))
    self.raise_for_status(res)
    return res


def delete_json(self, path, nosign=False):
    url = urljoin(self.base_uri, path)
    headers = {
        'Accept': FHIRJSONMimeType,
        'Accept-Charset': 'UTF-8',
    }
    # perform the request but intercept 401 responses, raising our own Exception
    res = self.session.delete(url)
    self.raise_for_status(res)
    return res

def _get(self, path, headers={}, nosign=False):
    """ Issues a GET request and returns response object """
    assert path
    url = urljoin(URIBASE, path)
    header_defaults = {
        'Accept': FHIRJSONMimeType,
        'Accept-Charset': 'UTF-8',
    }
    # merge in user headers with defaults
    header_defaults.update(headers)
    # use the merged headers in the request
    headers = header_defaults
        
    # perform the request but intercept 401 responses, raising our own Exception
    res = self.session.get(url, headers=headers)
    self.raise_for_status(res)
    return res