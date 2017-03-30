/**
 * Created by Shane Melton on 3/29/17.
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

import template from './dataUpload.html';
import './dataUpload.scss';

/**
 * Dependencies Array from imports
 */

let dependencies = [angularMeteor, uiRouter];

/**
 * The Page's component class. Instantiates any watchers, subscribes, and scope
 * of the page. Provides any methods that need to be accessed by the view.
 */
class DataUpload {

    constructor($reactive, $scope, $mdSidenav) {
        'ngInject';

        $reactive(this).attach($scope);

        this.subscribe('fileSchemas', () => [{
            viewName: "list"
        }]);

        this.selectedSchema = '';

        this.helpers({
            fileSchemas() {
                return FileSchemas.find({});
            }
        });

        this.$mdSidenav = $mdSidenav;

    }

    uploadFile() {

        let fd = new FormData();

        let url = "http://localhost:5000/post_file2";

        let xhr = new XMLHttpRequest();
        xhr.open('POST', url, true);
        xhr.onload = function(event){
          console.log(event);
        };

        fd.append('file', this.files[0]);
        fd.append('schema_name', this.selectedSchema);

        xhr.send(fd);

    }

}



//The angular name for this component
export const name = "upload";

//Export the actual component in its own module
export default angular.module(name, dependencies)
    .component(name, {
        template,
        controller: DataUpload,
        controllerAs: name
    })
    .directive('fileInput', function ($parse) {
        'ngInject';
        return {
            restrict: 'A',
            link: function (scope, element, attributes) {
                element.bind('change', function (event) {

                    console.log(element[0].files);
                    $parse(attributes.fileInput)
                        .assign(scope,element[0].files);
                    scope.$apply()
                });
            }
        };
    })
    .config(config);

/**
 * Config function that will configure the state and URL route for this page
 * @param $stateProvider
 */
function config($stateProvider) {
    'ngInject';

    $stateProvider
        .state('dataUpload', {
            url: '/upload',
            views: {
                'main': {
                    template: '<upload></upload>'
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
        });

}