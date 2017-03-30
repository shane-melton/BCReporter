from flask import Flask, abort, jsonify, request
from flask_cors import CORS, cross_origin
import json
from collections import OrderedDict
import sys
from pymongo import MongoClient
import csv
from detectors.load import *
from io import TextIOWrapper

app = Flask(__name__)
CORS(app)
mong_client_system = MongoClient('mongodb://127.0.0.1:3001')
mong_client_data = MongoClient('localhost', 3001)
sys_db = mong_client_system.meteor
data_db = mong_client_data.data

#Broken but maybe useful?
@app.route('/post_file', methods=['POST'])
@cross_origin()
def index():
    file = request.files['file']
    body = request.get_json()
    schema_id = body["schema_name"]
    raw = file.read()
    schema = get_file_schema(schema_id)
    return upload_file_to_db(raw, "test", schema)

#Working
@app.route('/post_file2', methods=['POST'])
@cross_origin()
def test():
    file = request.files['file']
    filename = file.filename

    file = TextIOWrapper(file, encoding='utf-8')

    schema_id = request.form["schema_name"]
    raw = csv.reader(file, delimiter=',')
    schema = get_file_schema(schema_id)
    return upload_file_to_db(raw, filename, schema)

def get_file_schema(schema_id):
    file_schemas = sys_db.fileSchemas
    schema = file_schemas.find_one({"name": schema_id})
    if schema:
        return schema
    else:
        return "problem"


def upload_file_to_db(file, filename, schema):
    # print(schema)
    cur_collection = data_db[schema['name']]
    cols = next(file)

    schema_cols = [d['name'] for d in schema['columns']]

    print(schema_cols)
    print(cols)

    for val in cols:
        if val not in schema_cols:
            return "problem"
    for row in file:
        cur_upload = dict()
        cur_upload["filename"] = filename
        for i in range(len(cols)):
            val = row[i]
            #TODO: Need a new way to reference schema structure
            #if schema[cols[i]]["secure"] is True:
                # encrypt val
            cur_upload[cols[i]] = val
        cur_collection.insert(cur_upload)
    load_applications(schema["name"], filename)
    return "no problem"

@app.route('/rule_schema/', methods=['POST'])
def new_rule_schema():
    body = request.get_json()
    rule_schema_id = body["rule_id"]
    # load_rule(rule_id)
    



if __name__ == '__main__':
    app.run(debug=True)
