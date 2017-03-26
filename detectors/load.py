# TODO: Replace with better import once hyphens are replaced with underscores
input_system = __import__('input-system-api.input_system', fromlist=['input_system'])
Database = input_system.Database

from detectors.rule_based_fraud_detector import RuleBasedFraudDetector


# FOR TESTING PURPOSES ONLY -- REMOVE WHEN A DATABASE IS AVAILABLE
Database.__init__ = lambda *args: None
Database.connect = lambda *args: None


def load_rule(rule_id):
    # STUB
    return None

    """
    Copy the rule found at rule_id in the rules table of the system DB to the analytics DB.

    TODO:
        Run the rule against existing applications and store violations in the notifications
        table of the system DB.

    param: rule_id, int, unique identifier of the new rule.
    return: ids of new violations, list of ints (or None),
        ids of new rule violations in the notifications table of the system DB.
    """

    data_db = Database('', '', '', '')
    system_db = Database('', '', '', '')
    analytics_db = Database('', '', '', '')

    data_db.connect()
    system_db.connect()
    analytics_db.connect()

    [rule, *extra] = system_db.select('rules', lhs='id', rhs=rule_id)
    if len(extra) > 0:
        print("Warning: Rule selection returned multiple rules. Only copying the first one found.")

    # TODO: the analytics_db will be a nosql database
    # TODO: Get columns and values from rule
    analytics_db.insert('rules', columns=[], values=[])


def load_applications(app_table_id):
    # STUB
    return []

    """
    Copy the rules found in the table with app_table_id in the data DB into the analytics DB, and
    then run all existing rules (that have compatible schema) against the new applications, storing
    any violatins in the notifications table of the system DB.

    param: app_table_id, int, unique identifier of the new table.
    return: ids of new violations, list of ints,
        ids of new rule violations in the notifications table of the system DB.
    """

    data_db = Database('', '', '', '')
    system_db = Database('', '', '', '')
    analytics_db = Database('', '', '', '')

    data_db.connect()
    system_db.connect()
    analytics_db.connect()

    # Select all rows from applications table
    applications = data_db.select('applications')

    # TODO: Get columns and values from applications
    analytics_db.insert('applications', columns=[], values=[])

    # TODO: Get rules from analytics_db
    detector = RuleBasedFraudDetector(single_app_rules={}, cross_app_rules={})

    # TODO: Get apps from applications
    violations = detector.apply_rules(apps=[])

    # TODO: Put violations in notifications table of system_db
    # TODO: Get ids of violations as we send them
    violation_ids = []
    for v in violations:
        system_db.insert('notifications', columns=[], values=[])

    return violation_ids

