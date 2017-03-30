/**
 * Created by shane on 3/23/17.
 */

import {Rules, RuleSchema} from './collection';

export function createRule(ruleObject) {

    RuleSchema.clean(ruleObject);

    check(ruleObject, RuleSchema);

    Rules.insert(ruleObject);

}

export function removeRule(ruleId) {

    check(ruleId, String);

    Rules.remove(ruleId);

}

export function saveRule(ruleId, ruleObject) {

    RuleSchema.clean(ruleObject);

    check(ruleId, String);
    check(ruleObject, RuleSchema);

    Rules.update(ruleId, {$set: {
        name: ruleObject.name,
        description: ruleObject.description,
        fileSchemaId: ruleObject.fileSchemaId,
        conditions: ruleObject.conditions
    }});

}

Meteor.methods({
    createRule,
    saveRule
});