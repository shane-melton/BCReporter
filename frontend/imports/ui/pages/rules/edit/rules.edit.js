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

    }

    hasConditions() {
        return !_.isEmpty(this.conditions);
    }

    hasFileSchema() {
        return !(_.isUndefined(this.fileSchema) || _.isNull(this.fileSchema));
    }

}
