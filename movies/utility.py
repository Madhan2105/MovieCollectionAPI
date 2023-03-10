from requests.adapters import HTTPAdapter
from urllib3 import Retry
import requests


class CustomSession(object):
    def __init__(self, url, username=None, password=None):
        self.session = requests.Session()
        if (username and password):
            self.session.auth = (username, password)
        adapter = HTTPAdapter(max_retries=Retry(total=4, backoff_factor=1,
                              allowed_methods=None,
                              status_forcelist=[429, 500, 502, 503, 504]))
        self.session.mount(url, adapter)

    def __enter__(self):
        return self.session

    def __exit__(self, type, value, traceback):
        self.session.close()
