from flask import Flask, abort, jsonify

app = Flask(__name__)


@app.route('/')
def index():
    return "Hello, World!"


@app.route('/file_column_schema/<int:file_column_id>', methods=['GET'])
def get_file_column_schema(file_column_id):
    return "" + file_column_id


@app.route('/file_schema_schema/', methods=['POST'])
def push_file_column_schema():
    if not request.json:
        abort(404)
    file_column_schema = request.json
    return jsonify({'file_column_schema': file_column_schema}), 200


@app.route('/upload_file/', methods=['POST'])
def push_upload_file():
    if not request.json:
        abort(404)
    upload_file = request.json
    return jsonify({'upload_file': upload_file}), 200


@app.route('/rule_schema/<int:rule_schema_id>', methods=['GET'])
def get_rule_schema(rule_schema_id):
    return "" + rule_schema_id


@app.route('/rule_schema/', methods=['POST'])
def push_rule_schema():
    if not request.json:
        abort(404)
    rule_schema = request.json
    return jsonify({'rule_schema': rule_schema}), 200


if __name__ == '__main__':
    app.run(debug=True)
