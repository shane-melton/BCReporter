import unittest
from input_system import InputSystem
import json
from collections import OrderedDict

data = []
with open('login.json') as data_file:
    data = json.load(data_file)
x = InputSystem(data, data)
a = '{ "id": "INTEGER", "name": "TEXT" }'
b = json.JSONDecoder(object_pairs_hook=OrderedDict).decode(a)
x.upload_file_column_schema("test", b.items(), "id")