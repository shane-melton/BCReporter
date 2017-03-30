/**
 * Created by shane on 3/20/17.
 */

import {Meteor} from 'meteor/meteor';

import {Notifications} from './collection';

if(Meteor.isServer) {

    Notifications.views = {};

    /**
     * A view that returns all FileSchemas sorted by the given parameter
     * @param params The parameter object
     * @param params.sort The object defining the sort criteria
     * @returns {{find: {}, options: {}}}
     */
    Notifications.views.list = function (params) {

        let options = {};

        if(_.isObject(params.sort) && !_.isEmpty(params.sort))
        {
            options.sort = params.sort;
        }

        return {
            find: {},
            options: options
        };

    };

    Notifications.views.edit = function (params) {

        if(_.isUndefined(params.id))
            throw new Error("bad-id", "An undefined ID was given to the FileSchema edit view!");

        return {
            find: params.id,
            options: {}
        };

    };

    function queryConstructor(parameters, userId) {

        let viewFunc = Notifications.views[parameters.viewName];
        let query = viewFunc(parameters);

        //Add any query requirements here that should span all views

        return query;
    }

    Meteor.publish('notifications', function(parameters) {

        check(parameters, Match.Maybe(Object));

        // if(!!this.userId) {

            if(_.isNull(parameters)) {
                parameters = {
                    viewName: "list"
                };
            }

            let query = queryConstructor(parameters, this.userId);

            return Notifications.find(query.find, query.options);
        // }

    });

}