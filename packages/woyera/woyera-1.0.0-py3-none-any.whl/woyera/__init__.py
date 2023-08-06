name = "woyera"

import requests
import json

class API:

    def __init__(self):
        self.accessKey = None
        self.secretKey = None
        self.url = "http://127.0.0.1:8080/api/"
        self.r = None

    def detect_defects(self, data, columnNames=None, clean=False, detectFunctions=None):
        data_dict = {'data': data}

        request_body = self.add_to_request_body(data_dict, columnNames, clean, detectFunctions)

        r = requests.post(self.url, json=json.loads(json.dumps(request_body)),
                          headers={'accessKey': self.accessKey, 'secretKey': self.secretKey})

        self.r = r

        return r

    def add_to_request_body(self, data, columnNames, clean, detectFunctions):
        data['clean'] = clean

        if columnNames is not None:
            data['columnNames'] = columnNames

        if detectFunctions is not None:
            data['detectFunctions'] = detectFunctions

        return data