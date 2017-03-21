from flask import Flask, abort, jsonify, request
from input_system import InputSystem
import json
from collections import OrderedDict

app = Flask(__name__)
in_sys = InputSystem()


@app.route('/', methods=['POST'])
def index():
    return "Hello World"


@app.route('/file_column_schema/<string:schema_name>', methods=['GET'])
def get_file_column_schema(schema_name):
    ret = in_sys.get_file_column_schema(schema_name)
    return str(ret)


@app.route('/file_column_schema/', methods=['POST'])
def push_file_column_schema():
    file_col_schema = request.get_json()
    if not file_col_schema:
        abort(404)
    schema_name = file_col_schema['schema_name']
    column_schema = json.JSONDecoder(object_pairs_hook=OrderedDict).decode(file_col_schema['column_schema'])
    primary_key = file_col_schema['primary_key']
    in_sys.upload_file_column_schema(schema_name, column_schema, primary_key)
    return "success", 200


@app.route('/upload_file/', methods=['POST'])
def push_upload_file():
    if not request.json:
        abort(404)
    upload_file = request.json
    return jsonify({'upload_file': upload_file}), 200


@app.route('/rule_schema/<string:rule_schema>', methods=['GET'])
def get_rule_schema(rule_schema):
    return "" + rule_schema


@app.route('/rule_schema/', methods=['POST'])
def push_rule_schema():
    rule_schema = request.get_json()
    if not data:
        abort(404)
    return jsonify({'rule_schema': rule_schema}), 200


if __name__ == '__main__':
    app.run(debug=True)
