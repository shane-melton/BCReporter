/**
 * Created by shane on 3/19/17.
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

        //Array of selected columns
        this.selected = [];

        //The schema
        this.schema = {};
        this.schema.columns = [];

        this.formTitle = "Create a New File Schema";
        this.newSchema = true;

        if(!_.isNull($stateParams.id)) {
            this.subscribe('fileSchemas', () => [{
                viewName: "edit",
                id: $stateParams.id
            }], {
                onReady: () => {
                    this.schema = FileSchemas.findOne($stateParams.id);
                    if(_.isUndefined(this.schema.columns)) {
                        this.schema.columns = [];
                    }
                }
            });

            this.formTitle = "Edit Existing File Schema";
            this.newSchema = false;
        }

        //A new column schema that is attached each time the add button is pressed
        this.newColumnSchema = {
            id: 0,
            name: "",
            type: "Integer",
            unique: false,
            secure: false
        };

        //Allowed data types
        this.types = ["Integer", "String", "Float", "Boolean"];

        $timeout(() => {
            $('#schemaName').focus();
        },50);

    }

    save() {

        if(this.newSchema) {
            this.call('createSchema', this.schema, (err, result) => {
                if(!err) {
                    this.$mdToast.show(
                        this.$mdToast.simple()
                            .textContent("Schema Created Successfully!")
                            .position('top right')
                            .hideDelay(3000)
                    );

                    this.$state.go('fileSchemas.list');
                }
            });
        }
        else {
            this.call('saveSchema', this.$stateParams.id, this.schema, (err, result) => {
                if(!err) {
                    this.$mdToast.show(
                        this.$mdToast.simple()
                            .textContent("Schema Save Successfully!")
                            .position('top right')
                            .hideDelay(3000)
                    );

                    this.$state.go('fileSchemas.list');
                }
            });
        }




    }

    editColumnName(event, column) {
        event.stopPropagation();

        let editDialog = {
            modelValue: column.name,
            placeholder: 'Enter column name',
            save: function (input) {
                column.name = input.$modelValue;
            },
            targetEvent: event,
            title: 'Enter column name',
            validators: {
                'md-maxlength': 30
            }
        };

        let promise = this.$mdEditDialog.small(editDialog);

        let otherColumns = this.schema.columns;
        let $mdToast = this.$mdToast;

        let that = this;

        promise.then(function (ctrl) {
            let input = ctrl.getInput();

            input.$viewChangeListeners.push(function () {

                let isDuplicate = _.some(otherColumns, (other) => {
                   return other.name == input.$modelValue;
                });

                if(isDuplicate) {
                    $mdToast.show(
                        $mdToast.simple()
                            .textContent("Duplicate Column Name!")
                            .position('top right')
                            .hideDelay(3000)
                    );
                }



                input.$setValidity('Duplicate', !isDuplicate);



            });
        })


    }

    addColumn() {
        this.schema.columns.push(_.clone(this.newColumnSchema));
        this.newColumnSchema.id++;
    }

    deleteSelected() {
        this.schema.columns = _.reject(this.schema.columns, (item) => {
            return !_.isUndefined(_.findWhere(this.selected, {id: item.id}));
        });
        this.selected = [];
    }

}