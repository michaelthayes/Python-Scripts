# -*- coding: utf-8 -*-
"""
Created on Wed Apr 10 17:56:01 2024

@author: hayes
"""

import json
from datetime import datetime
from datetime import date

# Define a custom serializer for datetime objects
def datetime_serializer(obj):
    if isinstance(obj, datetime) or isinstance(obj, date):
        return obj.isoformat()
    # elif isinstance(obj, date):
    #     return obj.isoformat()
    raise TypeError(f"Type {type(obj)} not serializable")

# Define the dictionary to be serialized
data = "{ 'somethingDate': datetime(2024, 2, 4, 0, 0, 0), \
    'otherDate' : date(2024, 2, 4) }"

# Serialize the dictionary to a JSON string
serialized_data = json.dumps(eval(data), default=datetime_serializer)

# Print the serialized data
print(serialized_data)