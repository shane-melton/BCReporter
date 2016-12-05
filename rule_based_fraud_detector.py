import operator as op

class RuleBasedFraudDetector:
    operators = {
        '<': op.lt,
        '<=': op.le,
        '==': op.eq,
        '>=': op.ge,
        '>': op.gt,
        '!=': op.ne
    }

    def __init__(self):
        pass

    def satisfies_condition(self, condition, lhs, rhs):
        return self.operators[condition](lhs, rhs)

    def apply_rule(self, column, condition, value, application):
        if not self.satisfies_condition(condition, application[column], value):
            return (condition, column, value)
        return None

    def apply_rules(self, rules, application):
        violations = []
        for rule in rules:
            result = self.apply_rule(rule['column'], rule['condition'], rule['value'], application)
            if result: violations.append(result)
        return violations
