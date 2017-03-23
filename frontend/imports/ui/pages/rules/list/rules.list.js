/**
 * Created by shane on 3/23/17.
 */

// import {FileSchemas} from '../../../../api/fileSchemas';

export default class ListController {

    constructor($reactive, $scope, $state, $mdDialog) {
        'ngInject';

        this.$state = $state;
        this.$mdDialog = $mdDialog;

        $reactive(this).attach($scope);

    }

}