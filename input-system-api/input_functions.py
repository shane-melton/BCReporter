import psycopg2
from flask import jsonify


def get_file_column_schema(schema_name):
    try:
        conn = psycopg2.connect("dbname='' user='' host='' password=''")
    except:
        print("Error: Cannot connect to database")
        raise
    cur = conn.cursor()
    cur.execute("""SELECT schema FROM schemas WHERE schema_name =  {}""".format(schema_name))
    return jsonify({"schema": cur.fetchall()})


def push_file_column_schema(column_schema):
    try:
        conn = psycopg2.connect("dbname='' user='' host='' password=''")
    except:
        print("Error: Cannot connect to database")
        raise
    cur = conn.cursor()
    col_string = ""
    val_string = ""
    for col in column_schema["schema"]:
        col_string += "{} {} ".format(col[0], col[1])
        val_string += col[1] + " "
    cur.execute("""CREATE TABLE {}({} PRIMARY KEY({})) """.format(column_schema["schema_name"], col_string, column_schema["id_field"]))
    cur.execute("""INSERT INTO schemas VALUES ({})""".format(val_string))


def push_upload_file(file_information, file_schema):
    pass
