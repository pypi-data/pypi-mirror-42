import importlib
import json

import requests
from requests.auth import HTTPBasicAuth

from .models.error import ServerpilotError


class Serverpilot:
    client_id: str
    api_key: str

    BASE_URL = 'https://api.serverpilot.io/v1/{}'

    def __init__(self, client_id: str = '', api_key: str = '') -> None:
        if client_id is '' or api_key is '':
            raise ValueError('Client ID and API keys are required')

        self.client_id = client_id
        self.api_key = api_key

    def _request(self, method: str = '', endpoint: str = '', data: str or dict = None) -> dict:
        if data is None:
            data = {}

        headers = {
            'Content-Type': 'application/json',
        }

        response = requests.request(
            method,
            self.BASE_URL.format(endpoint),
            auth=HTTPBasicAuth(
                username=self.client_id,
                password=self.api_key
            ),
            data=json.dumps(data) if data != {} else {},
            headers=headers,
        )

        if response.status_code != 200:
            raise ServerpilotError(response.status_code, response.json()['error']['message'])

        return response.json()['data']

    @classmethod
    def client(cls, module_name: str = '', client_id: str = '', api_key: str = ''):
        module = importlib.import_module('pyserverpilot.modules')
        class_ = getattr(module, module_name.capitalize())

        return class_(client_id, api_key)
