/**
 * Created by shane on 3/20/17.
 */

import {Mongo} from 'meteor/mongo';

export const FileSchemas = new Mongo.Collection('fileSchemas');

if(Meteor.isServer) {
    FileSchemas.before.insert((userId, doc) => {
        doc.dateCreated = Date.now();
    });
}

export const ColumnSchema = new SimpleSchema({
    name: {
        type: String
    },
    type: {
        type: String,
        allowedValues: ["Integer", "String", "Boolean", "Float"]
    },
    unique: {
        type: Boolean,
        defaultValue: false
    },
    secure: {
        type: Boolean,
        defaultValue: false
    }
});

export const FileSchemaSchema = new SimpleSchema({
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
    columns: {
        type: [ColumnSchema]
    }
});

FileSchemas.helpers({

});

FileSchemas.attachSchema(FileSchemaSchema);