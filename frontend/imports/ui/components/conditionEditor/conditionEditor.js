/**
 * Created by shane on 3/24/17.
 */

/**
 * Angular Imports
 */
import angular from 'angular';
import angularMeteor from 'angular-meteor';

/**
 * Meteor Imports
 */

/**
 * API Imports
 */

// import {Rules} from '../../../api/rules/';
import {DATA_TYPES} from '../../../api/fileSchemas';

/**
 * User Interface Imports
 */

/**
 * Component Imports
 */

import template from './conditionEditor.html';
import './conditionEditor.scss';

/**
 * Dependencies Array from imports
 */

let dependencies = [angularMeteor];

/**
 * The Navigation component's class and will provide the html with scope functions
 */
class ConditionEditor {

    constructor() {
        'ngInject';

        if(_.isUndefined(this.condition) || _.isNull(this.condition)) {
            this.condition = {};
        }

        this.fields = [{
            name: 'id',
            type: 'String'
        }, {
            name: 'lastName',
            type: 'String'
        }, {
            name: 'isSingle',
            type: 'Boolean'
        }, {
            name: 'income',
            type: 'Integer'
        }];

        this.comparisons = [{
            desc: 'less than',
            val: '<'
        }, {
            desc: 'equal to',
            val: '='
        }, {
            desc: 'greater than',
            val: '>'
        }];


    }

    fieldChange() {
        this.condition.value = null;
        if(this.condition.field.type == "Boolean") {
            this.condition.comparison = "=";
        }
        else {
            this.condition.comparison = null;
        }
    }

    isBoolean() {
        if(_.isUndefined(this.condition) || _.isUndefined(this.condition.field))
            return false;
        return this.condition.field.type == "Boolean";
    }



}

//The angular name for this component
export const name = "conditionEditor";

export default angular.module(name, dependencies)
    .component(name, {
        template,
        controller: ConditionEditor,
        controllerAs: '$ctrl',
        bindings: {
            'condition': '<'
        }
    })
    .config(config);

function config() {
    'ngInject';
}



