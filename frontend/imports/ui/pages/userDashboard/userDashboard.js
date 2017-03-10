/**
 * Created by Shane Melton on 2/10/17.
 *
 * User dashboard that is the main landing page for logged in users. It will provide
 * realtime information regarding the system, rules, alerts, etc.
 *
 */

/**
 * Angular Imports
 */
import angular from 'angular';
import angularMeteor from 'angular-meteor';
import uiRouter from 'angular-ui-router';

/**
 * Meteor Imports
 */

/**
 * API Imports
 */

/**
 * User Interface Imports
 */

/**
 * Page Imports
 */

import template from './userDashboard.html';
import './userDashboard.scss';

/**
 * Dependencies Array from imports
 */

let dependencies = [angularMeteor, uiRouter];

/**
 * The Page's component class. Instantiates any watchers, subscribes, and scope
 * of the page. Provides any methods that need to be accessed by the view.
 */
class UserDashboard {

    constructor($reactive, $scope, $mdSidenav) {
        'ngInject';

        this.$mdSidenav = $mdSidenav;

        console.log(template);

    }

    toggleUserList() {
        this.$mdSidenav('left').toggle();
    }

    doSomething() {
        console.log("Dtahsdf");
    }

}



//The angular name for this component
export const name = "userDashboard";

//Export the actual component in its own module
export default angular.module(name, dependencies)
    .component(name, {
        template,
        controller: UserDashboard,
        controllerAs: name
    })
    .config(config);

/**
 * Config function that will configure the state and URL route for this page
 * @param $stateProvider
 */
function config($stateProvider) {
    'ngInject';

    $stateProvider
        .state('userDashboard', {
            url: '/dash',
            views: {
                'main': {
                    template: '<user-dashboard></user-dashboard>'
                }
            }
        });

}