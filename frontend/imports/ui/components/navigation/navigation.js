/**
 * Created by Shane Melton on 2/10/17.
 *
 * The navigation bar and side-nav. It will be used across all pages and can be customized per page by defining a
 * template for the 'nav' view.
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
 * Component Imports
 */

import template from './navTemplate.html';
import './navigation.scss';

/**
 * Dependencies Array from imports
 */

let dependencies = [angularMeteor, uiRouter];

/**
 * The Navigation component's class and will provide the html with scope functions
 */
class Navigation {

    constructor($reactive, $scope, $mdSidenav) {
        'ngInject';

        this.$mdSidenav = $mdSidenav;

    }

    toggleSideNav() {
        this.$mdSidenav('left').toggle();
    }

}

//The angular name for this component
export const name = "navigation";


export default angular.module(name, dependencies)
    .component(name, {
        template,
        controller: Navigation,
        controllerAs: name
    })
    .config(config);

function config() {
    'ngInject';
}



