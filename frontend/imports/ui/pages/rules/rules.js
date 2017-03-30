/**
 * Created by shane on 3/23/17.
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

import {name as ConditionEditor} from '../../components/conditionEditor/conditionEditor';

/**
 * Page Imports
 */
import sideNavTemplate from '../../templates/default.sidenav.html';

import listTemplate from './list/rules.list.html';
import ListController from './list/rules.list';

import editTemplate from './edit/rules.edit.html';
import EditController from './edit/rules.edit';

import './rules.scss';

/**
 * Dependencies Array from imports
 */

let dependencies = [angularMeteor, uiRouter, ConditionEditor];

/**
 * The Page's component class. Instantiates any watchers, subscribes, and scope
 * of the page. Provides any methods that need to be accessed by the view.
 */
class RulesController {

    constructor($reactive, $scope) {
        'ngInject';

    }

}



//The angular name for this component
export const name = "rules";

//Export the actual component in its own module
export default angular.module(name, dependencies).config(config);

/**
 * Config function that will configure the state and URL route for this page
 * @param $stateProvider
 */
function config($stateProvider) {
    'ngInject';

    $stateProvider
        .state('rules', {
            abstract: true,
            url: '/rules',
            views: {
                'main': {
                    template: '<ui-view/>',
                    controller: RulesController,
                    controllerAs: '$page'
                },
                'sidenav': {
                    template: sideNavTemplate,
                    controller: ($scope, $mdSidenav) => {
                        $scope.closeSideNav = () => {
                            $mdSidenav('left').toggle();
                        };
                    }
                }
            }
        })
        .state('rules.list', {
            url: '/list',
            template: listTemplate,
            controller: ListController,
            controllerAs: '$ctrl'
        })
        .state('rules.edit', {
            url: '/edit/:id',
            template: editTemplate,
            controller: EditController,
            controllerAs: '$ctrl',
            params: {
                id: {
                    value: null,
                    squash: true
                }
            }
        });
}


