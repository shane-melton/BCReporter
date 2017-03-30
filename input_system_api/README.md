# Bristlecone Reporter Input System API

## How To Launch

Run the following commands

```./flask/scripts/python.exe app.py
```

After the command the application should be accessible from [localhost:5000](http://localhost:5000).

## Mongo Database Details


## Collection Details

All collections in the data db are created dynamically according to the file schema the collection is associated with.
Collections are named after their file schema, and each document in that collection refers to one row of one file.
Each document will, in addition to the data from the file itself, have a "file_name" attribute that explains which file it was uploaded from.

## Rest API Details

### Notification API

#### Post

Endpoint: `POST /post_file`

It is expected that A <form> tag is marked with enctype=multipart/form-data and an <input type=file> is placed in that form.

Body Parameters:
```javascript
{
  "schema_name": <string>
}
```
Returns: 
```javascript
{
  status_msg: "File uploaded successfully!"
}
````

Endpoint: `POST /rule_schema`

Body Parameters:
```javascript
{
  "rule_name": <string>
}
```
Returns: 
```javascript
{
  status_msg: "Analytics system started successfully!"
}
````
