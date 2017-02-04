import operator as op


class RuleBasedFraudDetector:
    def __init__(self, single_app_rules=dict(), cross_app_rules=dict()):
        self._single_app_rules = single_app_rules
        self._cross_app_rules = cross_app_rules

    def apply_rules(self, apps):
        single_app_violations = []
        cross_app_violations = []

        for rule in self._single_app_rules:
            for app in enumerate(apps):
                result = self._apply_single_app_rule(**rule, app=app[1])
                if result: single_app_violations.append((app[0],) + result)

        for rule in self._cross_app_rules:
            result = self._apply_cross_app_rule(**rule, apps=apps)
            if result: cross_app_violations.append(result)

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

