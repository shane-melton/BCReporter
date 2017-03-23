/**
 * Created by shane on 3/19/17.
 */

import {FileSchemas} from '../../../../api/fileSchemas';

export default class ListController {

    constructor($reactive, $scope, $state, $mdDialog) {
        'ngInject';

        this.$state = $state;
        this.$mdDialog = $mdDialog;

        $reactive(this).attach($scope);

        this.subscribe('fileSchemas', () => [{
            viewName: "list"
        }]);

        this.helpers({
            fileSchemas() {
                return FileSchemas.find({});
            }
        });

    }

    edit(schema) {
        this.$state.go('fileSchemas.edit', {id: schema._id});
    }

    remove(schema, ev) {

        var confirm = this.$mdDialog.confirm()
            .title('Are you sure?')
            .textContent('Deleting this file schema cannot be undone!')
            .ariaLabel('Confirmation')
            .targetEvent(ev)
            .ok('Delete Schema')
            .cancel('Cancel');

        this.$mdDialog.show(confirm).then(() => {
            this.call('removeSchema', schema._id);
        }, () => {});


    }

}