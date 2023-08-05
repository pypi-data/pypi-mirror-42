#!/usr/bin/python
  
import os
import requests

api_endpoint='https://my.incapsula.com/api/'

def getSiteStatus(site_id, api_id=os.environ.get('API_ID'), api_key=os.environ.get('API_KEY')):
    url=api_endpoint + 'prov/v1/sites/status'
    payload={'api_id': api_id,'api_key': api_key, 'site_id': site_id}
    r = requests.post(url, data=payload)
    return r.text
