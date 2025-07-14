import json

from Demos.mmapfile_demo import offset

from api_client import RingCentralClient
from datetime import datetime, timedelta, time

perPage= 1000

def get_tomorrows_date():
    today = datetime.now()
    tomorrow=today + timedelta(days=1)
    end_of_day=datetime.combine(tomorrow.date(),time.max).isoformat()
    return end_of_day

def fetch_call_logs(date_to=None):

    if date_to is None:
        date_to=get_tomorrows_date()

    endpoint = "/restapi/v1.0/account/~/call-log"
    queryParams = {
        'dateFrom': "2025-07-10T00:00:00.138Z",
        'dateTo': date_to,
        'type': 'Voice',
        'view': "Detailed",
        'perPage': perPage,
    }
    all_records = []
    rc = RingCentralClient()
    rc.login()
    while endpoint:
        logs_json=rc.get(endpoint=endpoint,queryParams=queryParams)
        jsonObj = logs_json.json_dict()
        records = jsonObj.get('records', [])
        all_records.extend(records)
        navigation = jsonObj.get('navigation', {})
        endpoint = navigation.get('nextPage', {}).get('uri', None)
    for record in all_records:
        print(json.dumps(record, indent=2, sort_keys=True))

fetch_call_logs()