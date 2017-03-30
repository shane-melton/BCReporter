import unittest
from detectors.rule_based_fraud_detector import RuleBasedFraudDetector


class TestRuleBasedFraudDetector(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        self.single_app_rules = [
            {
                'column': 'income',
                'condition': '>=',
                'value': 100}]
        self.cross_app_rules = [
            {
                'aggregation': 'count',
                'column': 'ssn-hash',
                'condition': '<=',
                'value': 3,
                'key': '123'}]

        self.single_good_app = {'income': 110, 'name': 'Bob', 'ssn-hash': '123'}
        self.single_bad_app = {'income': 90, 'name': 'Sally', 'ssn-hash': '456'}

        self.cross_good_apps = [
            self.single_good_app,
            self.single_good_app,
            self.single_good_app,
            self.single_bad_app]

        self.cross_bad_apps = self.cross_good_apps + [self.single_good_app]

        self.det = RuleBasedFraudDetector(self.single_app_rules, self.cross_app_rules)
        super(TestRuleBasedFraudDetector, self).__init__(*args, **kwargs)

    def test__satisfies_condition(self):
        sat = RuleBasedFraudDetector._satisfies_condition  # For brevity
        self.assertTrue(sat('<', 0, 1))

        self.assertTrue(sat('<=', 1, 1))
        self.assertTrue(sat('<=', 0, 1))

        self.assertTrue(sat('==', 1, 1))

        self.assertTrue(sat('>=', 1, 1))
        self.assertTrue(sat('>=', 1, 0))

        self.assertTrue(sat('>', 1, 0))

        self.assertTrue(sat('!=', 0, 1))

    # Temporarily disabled
    def test__apply_single_app_rule(self):
        pass
        # self.assertEqual(
        #     self.det._apply_single_app_rule(**(self.single_app_rules[0]), app=self.single_good_app),
        #     None)
        #
        # self.assertEqual(
        #     self.det._apply_single_app_rule(**(self.single_app_rules[0]), app=self.single_bad_app),
        #     ('>=', 'income', 100))

    # Temporarily disabled
    def test__apply_cross_app_rule(self):
        pass
        # self.assertEqual(
        #     self.det._apply_cross_app_rule(
        #         **(self.cross_app_rules[0]),
        #         apps=self.cross_good_apps),
        #     None)
        #
        # self.assertEqual(
        #     self.det._apply_cross_app_rule(
        #         **(self.cross_app_rules[0]),
        #         apps=self.cross_bad_apps),
        #     ('<=', 'count', '123', 'ssn-hash', 3))

    # Temporariliy disabled
    def test_apply_rules(self):
        pass
    #     self.assertEqual(
    #         self.det.apply_rules(self.cross_good_apps),
    #         ([(3, '>=', 'income', 100)], []))
    #
    #     self.assertEqual(
    #         self.det.apply_rules(self.cross_bad_apps),
    #         ([(3, '>=', 'income', 100)], [('<=', 'count', '123', 'ssn-hash', 3)]))


if __name__ == '__main__':
    unittest.main()
