/**
 * Created by shane on 3/23/17.
 */

import {Mongo} from 'meteor/mongo';

import {FileSchemas} from '../fileSchemas';

export const Rules = new Mongo.Collection('rules');

if(Meteor.isServer) {
    Rules.before.insert((userId, doc) => {
        doc.dateCreated = Date.now();
    });
}

export const COMPARISON_OPS = ['=', '!=', '<', '<=', '>=', '>'];

export const ConditionSchema = new SimpleSchema({
    _id: {
        type: String,
        optional: true
    },
    fieldName: {
        type: String,
        label: "Field Name"
    },
    compValue: {
        type: String,
        label: "Comparison Value"
    },
    compOp: {
        type: String,
        label: "Comparison Operator",
        allowedValues: COMPARISON_OPS
    }
});

export const RuleSchema = new SimpleSchema({
    _id: {
        type: String,
        optional: true
    },
    dateCreated: {
        type: Date,
        optional: true
    },
    name: {
        type: String
    },
    description: {
        type: String,
        optional: true
    },
    fileSchemaId: {
        type: String,
        label: "Referenced FileSchema ID"
    },
    conditions: {
        type: [ConditionSchema],
        defaultValue: []
    }
});

Rules.helpers({
    FileSchema() {
        return FileSchemas.findOne(this.fileSchemaId);
    }
});

Rules.attachSchema(RuleSchema);