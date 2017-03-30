/**
 * Created by shane on 3/20/17.
 */

import {Meteor} from 'meteor/meteor';

import {FileSchemas} from './collection';

if(Meteor.isServer) {

    FileSchemas.views = {};

    /**
     * A view that returns all FileSchemas sorted by the given parameter
     * @param params The parameter object
     * @param params.sort The object defining the sort criteria
     * @returns {{find: {}, options: {}}}
     */
    FileSchemas.views.list = function (params) {

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

    FileSchemas.views.edit = function (params) {

        if(_.isUndefined(params.id))
            throw new Error("bad-id", "An undefined ID was given to the FileSchema edit view!");

        return {
            find: params.id,
            options: {}
        };

    };

    function queryConstructor(parameters, userId) {

        let viewFunc = FileSchemas.views[parameters.viewName];
        let query = viewFunc(parameters);

        //Add any query requirements here that should span all views

        return query;
    }

    Meteor.publish('fileSchemas', function(parameters) {

        check(parameters, Match.Maybe(Object));

        // if(!!this.userId) {

            if(_.isUndefined(parameters)) {
                parameters = {
                    viewName: "list"
                };
            }

            let query = queryConstructor(parameters, this.userId);

            return FileSchemas.find(query.find, query.options);
        // }

    })

}