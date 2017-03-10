/** @author Shane Melton **/

/**
 * Angular Imports
 */
import angular from 'angular';
import angularMeteor from 'angular-meteor';
import ngMaterial from 'angular-material';
import ngAnimate from 'angular-animate';
import ngAria from 'angular-aria';
import uiRouter from 'angular-ui-router';

/**
 * Meteor Imports
 */
import {Meteor} from 'meteor/meteor';

/**
 * Application Imports
 */

import 'angular-material/angular-material.css';
// import 'material-design-icons/iconfont/MaterialIcons-Regular.svg';

//Pages
import {name as UserDashboard} from '../imports/ui/pages/userDashboard/userDashboard';

//Components
import {name as Navigation} from '../imports/ui/components/navigation/navigation';

//Services

//API

let appName = "bcreporter";

let dependencies = [appName, angularMeteor, ngMaterial, ngAnimate, ngAria, uiRouter,
                    UserDashboard,
                    Navigation];

function config($locationProvider) {
    'ngInject';

    $locationProvider.html5Mode(true);

}

function run() {
    'ngInject';
}

function onReady() {

    angular.module(appName, dependencies)
        .config(config)
        .run(run);

    angular.bootstrap(document, dependencies, {
        strictDi: true
    });
}

if (Meteor.isCordova) {
    angular.element(document).on('deviceready', onReady);
} else {
    angular.element(document).ready(onReady);
}


