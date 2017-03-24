/**
 * Created by shane on 3/18/17.
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

import {FileSchemas} from '../../../api/fileSchemas';

/**
 * User Interface Imports
 */

/**
 * Page Imports
 */
import sideNavTemplate from '../../templates/default.sidenav.html'

import listTemplate from './list/fileSchemas.list.html';
import ListController from './list/fileSchemas.list';

import editTemplate from './edit/fileSchemas.edit.html';
import EditController from './edit/fileSchemas.edit';

import './fileSchemas.scss';

/**
 * Dependencies Array from imports
 */

let dependencies = [angularMeteor, uiRouter];

/**
 * The Page's component class. Instantiates any watchers, subscribes, and scope
 * of the page. Provides any methods that need to be accessed by the view.
 */
class FileSchemasController {

    constructor($reactive, $scope) {
        'ngInject';
        // $reactive(this).attach($scope);
    }

}



//The angular name for this component
export const name = "fileSchemas";

//Export the actual component in its own module
export default angular.module(name, dependencies).config(config);

/**
 * Config function that will configure the state and URL route for this page
 * @param $stateProvider
 */
function config($stateProvider) {
    'ngInject';

    $stateProvider
        .state('fileSchemas', {
            abstract: true,
            url: '/schemas',
            views: {
                'main': {
                    template: '<ui-view/>',
                    controller: FileSchemasController,
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
        .state('fileSchemas.list', {
            url: '/list',
            template: listTemplate,
            controller: ListController,
            controllerAs: '$ctrl'
        })
        .state('fileSchemas.edit', {
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


