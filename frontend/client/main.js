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
import 'angular-material-data-table';
import 'angular-material-data-table/dist/md-data-table.min.css';
// import 'material-design-icons/iconfont/MaterialIcons-Regular.svg';

//Pages
import {name as UserDashboard} from '../imports/ui/pages/userDashboard/userDashboard';
import {name as FileSchemas} from '../imports/ui/pages/fileSchemas/fileSchemas';
import {name as Rules} from '../imports/ui/pages/rules/rules';

//Components
import {name as Navigation} from '../imports/ui/components/navigation/navigation';

//Services

//API

import './main.scss';

let appName = "bcreporter";

let dependencies = [appName, angularMeteor, ngMaterial, ngAnimate, ngAria, uiRouter, 'md.data.table',
                    UserDashboard, FileSchemas, Rules,
                    Navigation];

function config($locationProvider, $urlRouterProvider) {
    'ngInject';

    $locationProvider.html5Mode(true);

    $urlRouterProvider.otherwise('/dash');

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


