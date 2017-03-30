# Bristlecone Reporter Frontend

## How To Launch

Nodejs v4.6.2 and [Meteorjs](https://www.meteor.com/) are required to run this web application. The easiest way to download the correct version of NodeJs is through [NVM](https://github.com/creationix/nvm).

After those are installed simply navigate to this folder and run the following:

```bash
  npm install #Install node modules
  meteor      #Install and launch meteor
```

After the `meteor` command the application should be accessible from [localhost:3000](http://localhost:3000).

## Mongo Database Details

The mongo database that Meteor creates can be connected to external using a Mongodb url. This can be found running the `meteor mongo -U` in the root directory of the Meteor app (frontend).

The default database that will have the fileschemas and rules is simply called `meteor`. So a command such as `use meteor` in a mongo CLI interpreter should switch to the correct database.

## Collection Details

### FileSchemas

The FileSchemas collection is called `fileSchemas` and it has the following structure which can be found in [FileSchema collection file](./imports/api/fileSchemas/collection.js).

```javascript
//FileSchema
{
    _id: {
        type: String,
        optional: true
    },
    dateCreated: {
        type: Date,
        optional: true
    },
    name: {
        type: String
    },
    description: {
        type: String,
        optional: true
    },
    columns: {
        type: [ColumnSchema]
    }
}
//ColumnSchema
{
    name: {
        type: String
    },
    type: {
        type: String,
        allowedValues: DATA_TYPES
    },
    unique: {
        type: Boolean,
        defaultValue: false
    },
    secure: {
        type: Boolean,
        defaultValue: false
    }
}
```

### Rules

The FileSchemas collection is called `rules` and it has the following structure which can be found in [Rules collection file](./imports/api/rules/collection.js).

```javascript
//RuleSchema
{
    _id: {
        type: String,
        optional: true
    },
    dateCreated: {
        type: Date,
        optional: true
    },
    name: {
        type: String
    },
    description: {
        type: String,
        optional: true
    },
    fileSchemaId: {
        type: String,
        label: "Referenced FileSchema ID"
    },
    conditions: {
        type: [ConditionSchema],
        defaultValue: []
    }
}
//ConditionSchema
{
    _id: {
        type: String,
        optional: true
    },
    fieldName: {
        type: String,
        label: "Field Name"
    },
    compValue: {
        type: String,
        label: "Comparison Value"
    },
    compOp: {
        type: String,
        label: "Comparison Operator",
        allowedValues: COMPARISON_OPS
    }
}
```

## Rest API Details

### Notification API

#### Post

Endpoint: `POST /api/notifications`
Body Parameters:
```javascript
{
  rule_id:  <ID of the triggered rule>
  app_id:   <ID of the data that triggered the rule>
}
```
Returns: 
```javascript
{
  status_msg: "Notification Created Successfully!"
}
````
