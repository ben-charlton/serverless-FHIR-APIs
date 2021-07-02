import json
import requests
import urllib
import logging
from urllib.parse import urljoin

# default type is fhir+json, as the server will only support JSON objects (for now)
FHIRJSONMimeType = 'application/fhir+json'
URIBASE = 'base uri for server here'

def get_json(self, path, nosign=False):
    """ Perform a GET request for JSON data against the server's base with the
    given relative path. """
    
    headers = {'Accept': 'application/json'}
    res = self._get(path, headers, nosign)
    return res.json()

def post_json(self, path, resource_json, nosign=False):
    """ Performs a POST of the given JSON, which should represent a
    resource, to the given relative path. """
    
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
    """ Issues a DELETE command against the given relative path, accepting
    a JSON response. """
    
    url = urljoin(self.base_uri, path)
    headers = {
        'Accept': FHIRJSONMimeType,
        'Accept-Charset': 'UTF-8',
    }
    if not nosign and self.auth is not None and self.auth.can_sign_headers():
        headers = self.auth.signed_headers(headers)
        
    # perform the request but intercept 401 responses, raising our own Exception
    res = self.session.delete(url)
    self.raise_for_status(res)
    return res

def _get(path, headers={}, nosign=False):
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
    if not nosign and self.auth is not None and self.auth.can_sign_headers():
        headers = self.auth.signed_headers(headers)
        
    # perform the request but intercept 401 responses, raising our own Exception
    res = self.session.get(url, headers=headers)
    self.raise_for_status(res)
    return res