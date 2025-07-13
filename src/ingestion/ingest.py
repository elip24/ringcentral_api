import json
import sys
import configparser

from httpx import HTTPError
from datetime import datetime, timedelta, time
from src.config.settings import api_creds
from ringcentral import SDK
from ringcentral.http.api_exception import ApiException

rcsdk = SDK(
    api_creds['clientId'],
    api_creds['clientSecret'],
    api_creds['server']
)
platform = rcsdk.platform()

def get_tomorrows_date():
    today = datetime.now()
    tomorrow=today + timedelta(days=1)
    end_of_day=datetime.combine(tomorrow.date(),time.max).isoformat()
    return end_of_day


def read_user_calllog(dateFrom=None, date_to=None):
    """ Parameters
   ----------
   dateFrom : datetime, optional
       A datetime to look up since so that we dont choke the API. If ommited, put it manually (in the case that we need
         to look since the start of a certain date).
   dateTo : datetime, optional
        A datetime to look up to so that we dont choke the API. If ommited, put it manually (in the case that we need
         to look since the start of a certain date)
   """

    if date_to is None:
        date_to = "2025-07-10T23:59:59.788Z"

    try:
        queryParams = {
            'dateFrom': "2025-07-10T00:00:00.138Z",
            'dateTo': "2025-07-10T22:00:00.138Z",
            'type': 'Voice',
            'view': "Detailed",
            'perPage': 1000
        }
        endpoint = "/restapi/v1.0/account/~/call-log"
        all_records=[]
        while endpoint:
            resp = platform.get(endpoint, queryParams)
            jsonObj = resp.json_dict()
            records = jsonObj.get('records', [])
            all_records.extend(records)
            navigation = jsonObj.get('navigation', {})
            endpoint = navigation.get('nextPage', {}).get('uri', None)

            queryParams = {}
        for record in all_records:
            print(json.dumps(record, indent=2, sort_keys=True))

    except Exception as e:
        print("Unable to read user call log. " + str(e))
        raise

def login():
    try:
        platform.login(jwt=api_creds['jwt'])
        read_user_calllog()

    except ApiException as e:
        error_message=e.api_response()._response.text
        error_json = json.loads(error_message)
        error_description=error_json.get("error_description")
        error_code = e.api_response()._response.status_code

login()