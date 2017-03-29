import pymongo
from pymongo import MongoClient

from detectors.rule_based_fraud_detector import RuleBasedFraudDetector


def load_rule(rule_id, mongo_host=None, mongo_port=None):
    """
    Copy the rule found at rule_id in the rules table of the system DB to the analytics DB.

    TODO:
        Run the rule against existing applications and store violations in the notifications
        table of the system DB.

    param: rule_id, int, unique identifier of the new rule.
    return: ids of new violations, list of ints (or None),
        ids of new rule violations in the notifications table of the system DB.
    """

    client = MongoClient(mongo_host, mongo_port)

    system_db = client.system_db
    analytics_db = client.analytics_db

    rule = system_db.rules.find_one({'_id':rule_id})
    analytics_db.rules.insert_one(rule)

    return None


def load_applications(app_table_id, mongo_host=None, mongo_port=None):
    """
    Copy the applications found in the table with app_table_id in the data DB into the analytics DB,
    and then run all existing rules (that have compatible schema) against the new applications,
    storing any violatins in the notifications table of the system DB.

    param: app_table_id, string, unique identifier of the new table.
    return: ids of new violations, list of ObjectId,
        ids of new rule violations in the notifications table of the system DB.
    """

    client = MongoClient(mongo_host, mongo_port)

    data_db = client.data_db
    system_db = client.system_db
    analytics_db = client.analytics_db

    # Copy over the new applications
    applications = list(data_db[app_table_id].find())
    analytics_db.applications.insert_many(applications)

    # Make detector with rules from analytics database
    # TODO: Enable cross-app rules
    rules = list(analytics_db.rules.find())
    detector = RuleBasedFraudDetector(single_app_rules=rules, cross_app_rules=None)

    # Run all rules against the new applications
    violations = detector.apply_rules(apps=applications)

    # Put violations in notifications table of system_db
    violations_insert_result = system_db.notifications.insert_many(violations)
    return violation_insert_result.inserted_ids

