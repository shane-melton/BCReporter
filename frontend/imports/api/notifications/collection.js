/**
 * Created by shane on 3/20/17.
 */

import {Mongo} from 'meteor/mongo';

export const Notifications = new Mongo.Collection('notifications');

if(Meteor.isServer) {
    Notifications.before.insert((userId, doc) => {
        doc.dateCreated = Date.now();
    });
}

export const NotificationSchema = new SimpleSchema({
    _id: {
        type: String,
        optional: true
    },
    dateCreated: {
        type: Date,
        optional: true
    },
    ruleId: {
        type: String
    },
    dataId: {
        type: String
    },
    isNew: {
        type: Boolean
    }
});

Notifications.helpers({

});

Notifications.attachSchema(NotificationSchema);