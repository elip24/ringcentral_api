import json
from Demos.mmapfile_demo import offset
import pickle

from .api_client import RingCentralClient
from datetime import datetime, timedelta, time, timezone, date
import time as time_module

from .aux import month_year_iter, get_last_date_of_month

perPage= 1000

def get_tomorrows_date():
    today = datetime.now()
    tomorrow=today + timedelta(days=1)
    end_of_day=datetime.combine(tomorrow.date(),time.max).isoformat()
    return end_of_day




def fetch_call_logs(first_datetime, last_datetime):
    endpoint = "/restapi/v1.0/account/~/call-log"
    queryParams = {
        'dateFrom': first_datetime,
        'dateTo': last_datetime,
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
    return all_records

def ingestion():
    month_data = fetch_call_logs(first_datetime='2025-08-01T00:00:00.000Z"', last_datetime='2025-08-08T23:59:59.999Z"')
    file_name = f"ringcentral_{y:04d}_{m:02d}.json"
    with open(file_name, "w", encoding="utf-8") as f:
        json.dump(month_data, f, ensure_ascii=False, indent=2)
    print(f"Done with {file_name}")

ingestion()