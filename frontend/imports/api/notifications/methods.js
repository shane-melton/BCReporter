/**
 * Created by shane on 3/20/17.
 */

import {Notifications} from './collection';

export function clearNotifications(notificationIds) {

    if(!_.isArray(notificationIds))
        notificationIds = [notificationIds];

    check(notificationIds, [String]);

    let query = {_id: {$in: notificationIds}};

    console.log(query);

    Notifications.update(query, {$set: {isNew: false}});

}

Meteor.methods({
    clearNotifications
});