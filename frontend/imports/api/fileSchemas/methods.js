/**
 * Created by shane on 3/20/17.
 */

import {FileSchemas, FileSchemaSchema} from './collection';

export function createSchema(schema) {
    FileSchemaSchema.clean(schema);

    check(schema, FileSchemaSchema);

    FileSchemas.insert(schema);
}

export function saveSchema(schemaId, schema) {

    FileSchemaSchema.clean(schema);

    check(schemaId, String);
    check(schema, FileSchemaSchema);

    FileSchemas.update(schemaId, {$set: {
        name: schema.name,
        description: schema.description,
        columns: schema.columns
    }});

}

export function removeSchema(schemaId) {

    check(schemaId, String);

    FileSchemas.remove(schemaId);

}


export function uploadData(formData) {

    check(formData, Object);

    if(Meteor.isServer) {

    let url = "http://localhost:5000/post_file";

    console.log("data", formData);


        // HTTP.call('POST', url, {
        //     data: formData,
        //     // headers: {
        //     //     'content-type': undefined
        //     // }
        // }, (data) => {
        //     console.log(data);
        // });
    }

}

Meteor.methods({
    saveSchema,
    createSchema,
    removeSchema,
    uploadData
});