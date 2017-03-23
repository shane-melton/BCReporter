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

export const CriteriaSchema = new SimpleSchema({
    _id: {
        type: String,
        optional: true
    },
    LHS: {
        type: String,
        label: "Left Hand Side"
    },
    RHS: {
        type: String,
        label: "Right Hand Side"
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
    criteria: {
        type: [CriteriaSchema],
        defaultValue: []
    }
});

RuleSchema.helpers({
    FileSchema() {
        return FileSchemas.findOne(this.fileSchemaId);
    }
});

Rules.attachSchema(RuleSchema);