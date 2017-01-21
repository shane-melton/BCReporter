import unittest
from detectors.rule_based_fraud_detector import RuleBasedFraudDetector


class TestRuleBasedFraudDetector(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        print("init")
        super(TestRuleBasedFraudDetector, self).__init__(*args, **kwargs)

    def test__satisfies_condition(self):
        # stub
        pass

    def test__apply_single_app_rule(self):
        # stub
        pass

    def test__apply_cross_app_rule(self):
        # stub
        pass

    def test_apply_rules(self):
        # stub
        pass

if __name__ == '__main__':
    unittest.main()
