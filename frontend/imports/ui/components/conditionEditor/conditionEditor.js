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

import {DATA_TYPES, FileSchemas} from '../../../api/fileSchemas';

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

        if(_.isUndefined(this.schema) || _.isNull(this.schema)) {
            this.schema = {
                columns: []
            }
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
        if(this.getField(this.condition.fieldName).type == "Boolean") {
            this.condition.compOp = "=";
        }
        else {
            this.condition.compOp = null;
        }
    }

    getField(fieldName) {
        return _.findWhere(this.schema.columns, {name: fieldName});
    }

    isBoolean() {
        if(_.isUndefined(this.condition) || _.isUndefined(this.condition.fieldName))
            return false;
        return this.getField(this.condition.fieldName).type == "Boolean";
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
            'condition': '<',
            'schema': '<'
        }
    })
    .config(config);

function config() {
    'ngInject';
}



