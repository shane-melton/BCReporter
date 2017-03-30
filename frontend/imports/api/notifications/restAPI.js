/**
 * Created by Shane Melton on 3/29/17.
 */

import {Notifications} from './collection';

if(Meteor.isServer) {

    let Api = new Restivus({
        useDefaultAuth: false,
        prettyJson: true
    });

    Api.addRoute('notifications/', {}, {
        post: function () {

            let notification = {
                ruleId: this.bodyParams.rule_id,
                dataId: this.bodyParams.app_id,
                isNew: true
            };

            Notifications.insert(notification);

            return {status_msg: "Notification Created Successfully!"};
        }
    });

}