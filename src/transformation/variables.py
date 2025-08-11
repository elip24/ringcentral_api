import pylab as pl
from polars import String, Int64, Struct, Float64, List, Boolean, Datetime

record_of_from_columns_name = [
    'phoneNumber','extensionNumber','extensionId','name','location','device','dialresPhoneNumber'
]
record_of_to_columns_name = [
    'phoneNumber','extensionNumber','extensionId','name','location','device','dialresPhoneNumber'
]
record_of_extension_columns_name = ['id','url']
record_from_device_column_name = ['id']
columns_available = []

column_to_use = (
    [
        "id", "direction", "duration[sec]", "result", "startTime", "action",
        "type", "lastModifiedTime", "partyId", "sessionId", "internalType",
        "reason", "reasonDescription", "telephonySessionId", "startDate", "syncstartdatetime",
    ]
    + [f"from_{field}" for field in record_of_from_columns_name if field != 'device']
    + [f"to_{field}" for field in record_of_to_columns_name]
    + [f"from_device_{field}" for field in record_from_device_column_name]
)



schema={'uri': String,
        'id': String,
        'sessionId': String,
        'startTime': String,
        'duration': Int64,
        'durationMs': Int64,
        'type': String,
        'internalType': String,
        'direction': String,
        'action': String,
        'result': String,
        'to': Struct({'name': String, 'phoneNumber': String, 'location': String}),
        'from': Struct({'name': String, 'phoneNumber': String, 'extensionId': String, 'device': Struct({'uri': String, 'id': String}), 'location': String}),
        'reason': String,
        'reasonDescription': String,
        'telephonySessionId': String,
        'partyId': String,
        'transport': String,
        'lastModifiedTime': String,
        'billing': Struct({'costIncluded': Float64, 'costPurchased': Float64}),
        'legs': List(
            Struct({'startTime': String, 'duration': Int64, 'durationMs': Int64, 'type': String,
                    'internalType': String, 'direction': String, 'action': String, 'result': String,
                    'to': Struct({'name': String, 'phoneNumber': String, 'location': String,
                                  'extensionId': String, 'extensionNumber': String}),
                    'from': Struct({'name': String, 'phoneNumber': String, 'extensionId': String,
                                    'device': Struct({'uri': String, 'id': String}), 'location': String}),
                    'reason': String, 'reasonDescription': String, 'telephonySessionId': String,
                    'partyId': String, 'transport': String,
                    'billing': Struct({'costIncluded': Float64, 'costPurchased': Float64}),
                    'legType': String,
                    'master': Boolean, 'extension': Struct({'uri': String, 'id': Int64})})),
        'extension': Struct({'uri': String, 'id': Int64}),
        'syncstartdatetime': Datetime}
