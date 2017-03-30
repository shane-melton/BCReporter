/**
 * Created by shane on 3/23/17.
 */

import {Meteor} from 'meteor/meteor';

import {Rules} from './collection';

if(Meteor.isServer) {

    Rules.views = {};

    /**
     * A view that returns all rules sorted by the given parameter
     * @param params The parameter object
     * @param params.sort The object defining the sort criteria
     * @returns {{find: {}, options: {}}}
     */
    Rules.views.list = function (params) {

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

    Rules.views.edit = function (params) {

        if(_.isUndefined(params.id))
            throw new Error("bad-id", "An undefined ID was given to the FileSchema edit view!");

        return {
            find: params.id,
            options: {}
        };

    };

    function queryConstructor(parameters, userId) {

        let viewFunc = Rules.views[parameters.viewName];
        let query = viewFunc(parameters);

        //Add any query requirements here that should span all views

        return query;
    }

    Meteor.publish('rules', function(parameters) {

        check(parameters, Match.Maybe(Object));

        // if(!!this.userId) {

        if(_.isUndefined(parameters)) {
            parameters = {
                viewName: "list"
            };
        }

        let query = queryConstructor(parameters, this.userId);

        return Rules.find(query.find, query.options);
        // }

    })

}