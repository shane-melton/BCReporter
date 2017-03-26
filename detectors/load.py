

def load_rule(rule_id):
    """
    Copy the rule found at rule_id in the rules table of the system DB to the analytics DB.

    TODO:
        Run the rule against existing applications and store violations in the notifications
        table of the system DB.

    param: rule_id, int, unique identifier of the new rule.
    return: ids of new violations, list of ints (or None),
        ids of new rule violations in the notifications table of the system DB.
    """
    pass


def load_applications(app_table_id):
    """
    Copy the rules found in the table with app_table_id in the data DB into the analytics DB, and
    then run all existing rules (that have compatible schema) against the new applications, storing
    any violatins in the notifications table of the system DB.

    param: app_table_id, int, unique identifier of the new table.
    return: ids of new violations, list of ints,
        ids of new rule violations in the notifications table of the system DB.
    """
    pass
