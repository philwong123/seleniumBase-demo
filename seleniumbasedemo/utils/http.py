#!/usr/bin/env python3

import json
import requests


class HTTP(object):
    """ Basic methods for HTTP operations.

    get_json_response: get response in json format.

    Attributes:
        config: A dictionary of HTTP settings.
    """

    def __init__(self, config):
        self.config = config

    def get_json_response(self, method, protocal, resource, payload={}, headers={}):
        """

        """
        host = self.config.get('host')
        port = self.config.get('port')
        response = requests.request(
            method, f'{protocal}://{host}:{port}/{resource}', data=payload, headers=headers, verify=False)
        return response.json()
