/**
 * Created by Shane Melton on 3/29/17.
 */
import angular from 'angular';

import {Notifications} from '../../../api/notifications';

export const name = "$Notifications";

class $Notifications {
    constructor($reactive, $rootScope, $mdToast) {
        'ngInject';

        $reactive(this).attach($rootScope);

        this.subscribe('notifications', () => [{
            viewName: 'list'
        }]);

        this.helpers({
            notifications() {
                return Notifications.find({});
            },
            newNotifications() {
                return Notifications.find({isNew: true});
            }
        });

        this.autorun(() => {

                let newNotifcations = Notifications.find({isNew: true}).fetch();

                if(!_.isEmpty(newNotifcations)) {
                    _.each(newNotifcations, (not) => {
                        this.$mdToast.show(
                            this.$mdToast.simple()
                                .textContent('There was a notification!')
                                .position("top right")
                                .hideDelay(3000)
                        );
                    });

                    this.call('clearNotifications', _.pluck(newNotifcations, '_id'));
                }
        });

        this.$mdToast = $mdToast;

    }

    getNewNotifications() {
        return this.newNotifications;
    }

}

export default angular.module(name, []).service(name, $Notifications);