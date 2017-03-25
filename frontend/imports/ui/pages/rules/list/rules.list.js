/**
 * Created by shane on 3/23/17.
 */

// import {FileSchemas} from '../../../../api/fileSchemas';

export default class ListController {

    constructor($reactive, $scope, $state, $mdDialog, $mdSidenav) {
        'ngInject';

        this.$state = $state;
        this.$mdDialog = $mdDialog;
        this.$mdSidenav = $mdSidenav;

        $reactive(this).attach($scope);

        this.search = {
            text: "",
            user: "",
            minAlerts: 0,
            maxAlerts: 0,
            schema: null
        };

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

    }
}