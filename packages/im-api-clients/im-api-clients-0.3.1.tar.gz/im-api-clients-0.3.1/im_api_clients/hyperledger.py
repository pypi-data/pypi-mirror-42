import requests
from datetime import datetime
import os

class Client():

    def __init__(self, **kwargs):
        self.url = kwargs.get('url')
        self.query_url = kwargs.get('query_url')

    def request(self, method, *args, **kwargs):
        return getattr(self, method)(*args, **kwargs)

    def queries_list_sanctions_last_updated(self, last_updated):
        last_updated = last_updated.strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z"
        return requests.get(self.query_url, params = { 'lastUpdated': last_updated }).json()

    def get(self, id = None, **kwargs):
        full_url = self.url
        if id is not None:
            full_url = os.path.join(full_url, str(id))
        return requests.get(full_url, params = kwargs).json() 

    def bulk_get(self, ids = [], **kwargs):
        return [self.get(id, **kwargs) for id in ids]
    
    def post(self, record):
        r = requests.post(self.url, json = record)
        return r
    
    def bulk_post(self, records):
        for r in records:
            self.post(r)
    
    def put(self, id, record ):
        full_url = os.path.join(self.url, str(id)) 
        r = requests.put(full_url, json = record)
        return r
    
    def delete(self, id = None, record = None):
        id = id or record['internalId']
        full_url = os.path.join(self.url, str(id))
        r = requests.delete(full_url)
        return r
    
    def bulk_delete(self, ids = None, records = None):
        ids = ids or [x['id'] for x in records]
        for id in ids:
            self.delete(id)

    def head(self, id):
        full_url = os.path.join(self.url, str(id))
        r = requests.head(full_url)
        return r.status_code
    

