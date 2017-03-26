/**
 * Created by shane on 3/23/17.
 */

export default class EditController {

    constructor($reactive, $scope, $mdEditDialog, $mdToast, $stateParams, $state, $timeout) {
        'ngInject';

        $reactive(this).attach($scope);

        //Dialog used to edit table contents
        this.$mdEditDialog = $mdEditDialog;
        this.$mdToast = $mdToast;
        this.$state = $state;
        this.$stateParams = $stateParams;

        this.fileSchemas = [
            {
                name: "Loan Application"
            },
            {
                name: "Credit Card Application"
            },
            {
                name: "Car Loan Application"
            }
        ];

        this.fileSchema = this.fileSchemas[0].name;

        this.conditions = [];
        this.fields = ['id', 'lastName', 'firstName'];

        this.comparison = '';

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

    hasConditions() {
        return !_.isEmpty(this.conditions);
    }

    hasFileSchema() {
        return !(_.isUndefined(this.fileSchema) || _.isNull(this.fileSchema));
    }

    clearAll() {
        this.conditions = [];
    }

    deleteSelected() {
        this.conditions = _.filter(this.conditions, (cond) => {
            return !cond.checked;
        });
    }

    addCondition() {
        this.conditions.push({});
    }

}
