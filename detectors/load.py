import pymongo
from pymongo import MongoClient
import requests

from detectors.rule_based_fraud_detector import RuleBasedFraudDetector


def load_rule(
        rule_id,
        system_uri='mongodb://127.0.0.1:3001/meteor',
        analytics_uri=None):
    """
    Copy the rule found at rule_id in the rules table of the system DB to the analytics DB.

    TODO:
        Run the rule against existing applications and store violations in the notifications
        table of the system DB.

    param: rule_id, int, unique identifier of the new rule.
    param: system_uri, str, uri of system db
    param: analytics_uri, str, uri of analytics db
    return: None
    """

    system_db = MongoClient(system_uri).meteor
    rule = system_db.rules.find_one({'_id':rule_id})

    # TODO: Remove check once analytics db exists
    if analytics_uri is not None:
        analytics_db = MongoClient(analytics_uri).analytics_db
        analytics_db.rules.insert_one(rule)


def load_applications(
        data_collection_name,
        data_id,
        data_uri='mongodb://127.0.0.1:3001/datadb',
        system_uri='mongodb://127.0.0.1:3001/meteor',
        analytics_uri=None):
    """
    Copy the applications found in the table with app_table_id in the data DB into the analytics DB,
    and then run all existing rules (that have compatible schema) against the new applications,
    storing any violatins in the notifications table of the system DB.

    param: app_table_id, str, unique identifier of the new table.
    param: data_uri, str, uri of data db
    param: system_uri, str, uri of system db
    param: analytics_uri, str, uri of analytics db
    return: None
    """

    data_db = MongoClient(data_uri).data
    applications = list(data_db[data_collection_name].find({'filename': data_id}))

    # TODO: Remove check once analytics db exists
    if analytics_uri is not None:
        analytics_db = MongoClient(analytics_uri).analytics_db

        # Copy over the new applications
        analytics_db.applications.insert_many(applications)

        # Make detector with rules from analytics database
        # TODO: Enable cross-app rules
        system_db_rules = list(analytics_db.rules.find())
    else:
        system_db = MongoClient(system_uri).meteor
        system_db_rules = list(system_db.rules.find())

    # Convert rules from system db format to format expected by detector
    rules = []
    for system_db_rule in system_db_rules:
        _id = system_db_rule['_id']
        body = system_db_rule['conditions'][0] # I assume only one condition per rule
        rule = {
            '_id': _id,
            'condition': body['compOp'],
            'column': body['fieldName'],
            'value': body['compValue']}
        rules.append(rule)

    # Run all rules against the new applications
    detector = RuleBasedFraudDetector(single_app_rules=rules, cross_app_rules=None)
    violations = detector.apply_rules(apps=applications)
    violations = [{'app_id':v['app_id'], 'rule_id':v['rule_id']} for v in violations[0]]

    # Put violations in notifications table of system_db
    requests.post('http://localhost:3000/api/notifications', data=violations[0])

