import operator as op


class RuleBasedFraudDetector:
    def __init__(self, single_app_rules=dict(), cross_app_rules=dict()):
        self._single_app_rules = single_app_rules
        self._cross_app_rules = cross_app_rules

    def apply_rules(self, apps):
        single_app_violations = []
        cross_app_violations = []

        single_app_violation_keys = ['app_id', 'rule_id', 'condition', 'column', 'value']
        cross_app_violation_keys = [
            'app_ids', 'rule_id', 'condition', 'aggregation', 'key', 'column', 'value']

        for rule in self._single_app_rules:
            for app in apps:
                result = self._apply_single_app_rule(**rule, app=app)
                if result:
                    violation = dict(list(zip(
                        single_app_violation_keys,
                        (app['_id'], rule['_id']) + result)))
                    single_app_violations.append(violation)

        for rule in self._cross_app_rules:
            result = self._apply_cross_app_rule(**rule, apps=apps)
            if result:
                app_ids = [app['_id'] for app in apps]
                violation = dict(list(zip(
                    cross_app_violation_keys,
                    (app_ids, rule['_id']) + result)))
                cross_app_violations.append(violation)

        return (single_app_violations, cross_app_violations)

    @staticmethod
    def _get_operators():
        return {
            '<': op.lt,
            '<=': op.le,
            '==': op.eq,
            '>=': op.ge,
            '>': op.gt,
            '!=': op.ne}

    @staticmethod
    def _get_aggregations():
        return {
            'count': lambda column, key, apps: len(
                [x for x in (app[column] for app in apps) if x == key])}

    @classmethod
    def _satisfies_condition(cls, condition, lhs, rhs):
        return cls._get_operators()[condition](lhs, rhs)

    def _apply_single_app_rule(self, column, condition, value, app):
        if not self._satisfies_condition(condition, app[column], value):
            return (condition, column, value)
        return None

    def _apply_cross_app_rule(self, aggregation, column, condition, value, apps, **kwargs):
        satisfies = self._satisfies_condition(
            condition, self._get_aggregations()[aggregation](column, kwargs['key'], apps), value)
        if not satisfies:
            return (condition, aggregation, kwargs['key'], column, value)
        return None

