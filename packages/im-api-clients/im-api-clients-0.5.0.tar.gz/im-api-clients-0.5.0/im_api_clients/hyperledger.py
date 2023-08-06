import requests
from datetime import datetime
import os
from urllib.parse import urljoin


class Client():
    SANCTIONS_PATH = 'Sanctions'
    QUERIES_PATH = 'queries/'
    SCREENING_LOGS_PATH = 'ScrLogs'

    def __init__(self, **kwargs):
        self.root_url = kwargs.get('root_url')
        self.sanctions_url = urljoin(self.root_url, self.SANCTIONS_PATH)
        self.queries_url = urljoin(self.root_url, self.QUERIES_PATH)
        self.screening_logs_url = urljoin(self.root_url, self.SCREENING_LOGS_PATH)

    def request(self, method, *args, **kwargs):
        return getattr(self, method)(*args, **kwargs)

    def get(self, full_url, id = None, **kwargs):
        '''generic GET'''
        if id is not None:
            full_url = os.path.join(full_url, str(id))
        return requests.get(full_url, params = kwargs) 

    def bulk_get(self, full_url, ids = [], **kwargs):
        '''generic GET'''
        return [self.get(full_url, id, **kwargs) for id in ids]
    
    def post(self, full_url, record):
        '''generic POST'''
        return requests.post(full_url, json = record)
    
    def bulk_post(self, full_url, records):
        for r in records:
            self.post(full_url, r)
    
    def put(self, url, id, record ):
        full_url = os.path.join(url, str(id)) 
        return requests.put(full_url, json = record)
    
    def delete(self, url, id = None, record = None):
        '''generic DELETE'''
        id = id or record['internalId']
        full_url = os.path.join(url, str(id))
        return requests.delete(full_url)
    
    def bulk_delete(self, ids = None, records = None):
        ids = ids or [x['id'] for x in records]
        for id in ids:
            self.delete(id)

    def head(self, url, id):
        '''generic HEAD'''
        full_url = os.path.join(url, str(id))
        r = requests.head(full_url)
        return r.status_code
    
    def get_sanctions(self, id = None, **kwargs):
        '''GET sanctions'''
        return self.get(self.sanctions_url, id = id, params = kwargs) 

    def post_sanctions(self, record):
        '''POST sanctions'''
        return self.post(self.sanctions_url, record)

    def put_sanctions(self, id, record ):
        '''PUT sanctions'''
        return self.put(self.sanctions_url, id, record)

    def delete_sanctions(self, id = None, record = None):
        return self.delete(self.sanctions_url, id = id, record = record)

    def head_sanctions(self, id):
        '''HEAD sanctions'''
        return self.head(self.sanctions_url, id)

    def queries_list_sanctions_last_updated(self, last_updated):
        last_updated = last_updated.strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z"
        full_url = urljoin(self.queries_url, 'listSanctionsLastUpdated')
        return requests.get(full_url, params = { 'lastUpdated': last_updated })


    def get_screening_logs(self, id = None, **kwargs):
        '''GET ScreeningLogs'''
        return self.get(self.screening_logs_url, id = id, params = kwargs)

    def post_screening_logs(self, record):
        return requests.post(self.screening_logs_url, json = record)

