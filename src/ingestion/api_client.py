from ringcentral import SDK
from ringcentral.http.api_exception import ApiException
from src.config.settings import api_creds
import json
import logging

class RingCentralClient:
    def __init__(self):
        self.rcsdk = SDK(
            api_creds['clientId'],
            api_creds['clientSecret'],
            api_creds['server'])
        self.platform = self.rcsdk.platform()

    def _api_exception(self, e:ApiException):
        try:
            response = e.api_response()
            error_json = json.loads(response.text)
            error_description = error_json.get("error_description")
            error_code = response.status_code
            raise RuntimeError([error_description, error_code])
        except Exception as parse:
            raise RuntimeError([parse])

    def login(self):
        try:
            self.platform.login(jwt=api_creds['jwt'])
        except ApiException as e:
            self._api_exception(e,"Loging Failed")

    def get(self,endpoint,queryParams=None):
        try:
            return self.platform.get(endpoint, queryParams)

        except ApiException as e:
            self._api_exception(e,f"GET {endpoint} failed")