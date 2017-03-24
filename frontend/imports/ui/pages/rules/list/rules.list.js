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

    }

    openSearch() {
        this.$mdSidenav('search').toggle();
    }



}