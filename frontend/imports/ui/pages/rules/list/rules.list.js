/**
 * Created by shane on 3/23/17.
 */

import {Rules} from '../../../../api/rules';

export default class ListController {

    constructor($reactive, $scope, $state, $mdDialog, $mdSidenav) {
        'ngInject';

        this.$state = $state;
        this.$mdDialog = $mdDialog;
        this.$mdSidenav = $mdSidenav;

        $reactive(this).attach($scope);

        this.subscribe('rules', () => [{
            viewName: 'list'
        }]);

        this.helpers({
            rules() {
                return Rules.find({});
            }
        });

        this.search = {
            text: "",
            user: "",
            minAlerts: 0,
            maxAlerts: 0,
            schema: null
        };
    }

    edit(rule) {
        this.$state.go('rules.edit', {id: rule._id});
    }

    remove(rule, ev) {

        var confirm = this.$mdDialog.confirm()
            .title('Are you sure?')
            .textContent('Deleting this rule cannot be undone!')
            .ariaLabel('Confirmation')
            .targetEvent(ev)
            .ok('Delete Rule')
            .cancel('Cancel');

        this.$mdDialog.show(confirm).then(() => {
            this.call('removeRule', rule._id);
        }, () => {});


    }
}