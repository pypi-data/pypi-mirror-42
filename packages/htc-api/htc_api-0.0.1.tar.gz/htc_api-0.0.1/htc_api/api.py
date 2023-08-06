"""htc_api.api"""

import requests


class Client:
    def __init__(self, username, server_code, url='http://167.99.167.17', port=51337):
        url = 'http://localhost'
        self.username = username
        self.server_code = server_code

        url = url[:-1] if url.endswith('/') else url
        self.base_url = '{}:{}/'.format(url, str(port))

        self.session = requests.Session()
        self.session.headers['Content-Type'] = 'application/json'

    def solve(self, level_id, flag):
        payload = {
            'level_id': level_id,
            'flag': flag
        }
        r = self.session.request('POST', self.base_url + 'solve', json=payload)
        r.raise_for_status()
        return r.json()
