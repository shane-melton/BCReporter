from flask import Flask, abort, jsonify, request
import json
from collections import OrderedDict
import sys
from pymongo import MongoClient
from ..detectors.load import *

app = Flask(__name__)
mong_client_system = MongoClient('localhost', 3001)
mong_client_data = MongoClient('localhost', 5001)
sys_db = mong_client_system.meteor
data_db = mong_client_data.data


@app.route('/post_file', methods=['POST'])
def index():
    file = request.files['file']
    body = request.get_json()
    schema_id = body["schema_name"]
    raw = file.read()
    schema = get_file_schema(schema_id)
    upload_file_to_db(raw, "test", schema)
    return "Hello World"

def get_file_schema(schema_id):
    file_schemas = sys_db.fileSchemas
    schema = file_schemas.find_one({"name": schema_id})
    if schema:
        return schema["columns"]
    else:
        return "problem"


def upload_file_to_db(file, filename, schema):
    cur_collection = data_db[schema.name]
    cols = file[0]
    for val in cols:
        if val not in schema.keys():
            return "problem"
    for row in file:
        cur_upload = dict()
        cur_upload["filename"] = filename
        for i in range(len(cols)):
            val = row[i]
            if schema[cols[i]]["secure"] is True:
                # encrypt val
            cur_upload[cols[i]] = val
        cur_collection.insert(cur_upload)
    load_applications(schema["name"])
    return "no problem"

@app.route('/rule_schema/', methods=['POST'])
def new_rule_schema():
    body = request.get_json()
    rule_schema_id = body["rule_name"]



if __name__ == '__main__':
    app.run(debug=True)
