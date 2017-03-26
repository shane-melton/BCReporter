/**
 * Created by shane on 3/23/17.
 */

import {FileSchemas} from '../../../../api/fileSchemas';

export default class EditController {

    constructor($reactive, $scope, $mdEditDialog, $mdToast, $stateParams, $state, $timeout) {
        'ngInject';

        $reactive(this).attach($scope);

        //Dialog used to edit table contents
        this.$mdEditDialog = $mdEditDialog;
        this.$mdToast = $mdToast;
        this.$state = $state;
        this.$stateParams = $stateParams;

        this.subscribe('fileSchemas', () => [{
            viewName: 'list',
            sort: {'name': 1}
        }]);

        this.helpers({
           fileSchemas() {
               return FileSchemas.find({});
           }
        });

        this.ruleObject = {
            conditions: []
        };

    }

    hasConditions() {
        return !_.isEmpty(this.ruleObject.conditions);
    }

    hasFileSchema() {
        return !(_.isUndefined(this.ruleObject.fileSchema) || _.isNull(this.ruleObject.fileSchema));
    }

    getFileSchema() {
        return _.findWhere(this.fileSchemas, {_id: this.ruleObject.fileSchemaId});
    }

    clearAll() {
        this.ruleObject.conditions = [];
    }

    deleteSelected() {
        this.ruleObject.conditions = _.filter(this.ruleObject.conditions, (cond) => {
            return !cond.checked;
        });
    }

    saveRule() {
        this.call('createRule', this.ruleObject, (err) => {
            if(err) {
                this.$mdToast.show(
                    this.$mdToast.simple()
                        .textContent('There was a problem creating the rule!')
                        .position("top right")
                        .hideDelay(3000)
                );
            }
            else {
                this.$mdToast.show(
                    this.$mdToast.simple()
                        .textContent('Rule created successfully!')
                        .position("top right")
                        .hideDelay(3000)
                );
            }
        });
    }

    addCondition() {
        if(_.isUndefined(this.ruleObject.fileSchemaId) || _.isEmpty(this.ruleObject.fileSchemaId)) {
            $('#schemaSelector').focus();
            this.$mdToast.show(
                this.$mdToast.simple()
                    .textContent('Please select a File Schema first!')
                    .position("top right")
                    .hideDelay(3000)
            );
            return;
        }

        this.ruleObject.conditions.push({});
    }

}
