/**
 * Created by shane on 3/23/17.
 */

import {Rules, RuleSchema} from './collection';

export function createRule(ruleObject) {

    RuleSchema.clean(ruleObject);

    check(ruleObject, RuleSchema);

    Rules.insert(ruleObject);

}

Meteor.methods({
    createRule
});