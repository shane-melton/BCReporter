import csv
import json
import pymysql


class InputSystem:
    data_db = Database(_username="admin", _password="password", _host_location="localhost", _db="data")
    system_db = Database(_username="admin", _password="password", _host_location="localhost", _db="system")
    col_schema_table = "col_schemas"
    rule_table = "rules"
    file_col_table = "file_column"

    def __init__(self):
        pass

    def create_data_table(self, table_name, col_schema_name):
        if not self.data_db.select(table_name): # List is empty; table does not exist


    def upload_file(self, col_schema_name, file_location, table_name):
        self.create_data_table(table_name, col_schema_name)
        col_schema = self.get_col_schema(col_schema_name)
        columns = "col_schema, " + ", ".join(col_schema)
        with open(file_location, 'rb') as csvfile:
            self.data_db.insert()
            data = csv.reader(csvfile, delimeter=",")
            for row in data:
                values = col_schema_name + ", " + ", ".join(row)
                self.data_db.insert(table_name, columns, values)
        self.data_db.commit()

    def upload_col_schema(self, col_schema_name, col_schema):
        columns = "schema_name, schema"
        data = {"schema": col_schema}
        values = "%s, %s" % (col_schema_name, json.dumps(data))
        self.system_db.insert(self.col_schema_table, columns, values)
        self.system_db.commit()

    def upload_rule(self, col_schema_name, rule):
        columns = "col_schema, rule"
        values = "%s, %s" % (col_schema_name, json.dumps(rule))
        self.system_db.insert(self.rule_table, columns, values)
        self.system_db.commit()

    def get_col_schema(self, col_schema_name):
        return self.system_db.select(self.col_schema_table, query=col_schema_name)

    def get_data_for_schema(self, col_schema_name):
        items = list()
        tables = self.system_db.select(self.file_col_table, query="table_name", where="col_schema=%s" % col_schema_name)
        for table in tables:
            items = items + self.data_db.select(table)
        return items

    def get_rules_for_schema(self, col_schema_name):
        return self.system_db.select(self.rule_table, query="rule", where="col_schema=%s" % col_schema_name)


class Database:
    username = ""
    password = ""
    host_location = ""
    db = ""
    connected = False
    connection = object

    def __init__(self, _username, _password, _host_location, _db):
        self.username = _username
        self.password = _password
        self.host_location = _host_location
        self.db = _db
        self.connection, self.connected = self.connect()

    def connect(self):
        try:
            con = pymysql.connect(host=self.host_location, user=self.username, passwd=self.password, db=self.db)
            return [con, True]
        except Exception as e:
            return [e, False]

    def disconnect(self):
        if self.connected:
            self.connection.close()

    def insert(self, table, columns, values):
        if self.connected:
            with self.connection.cursor() as cursor:
                sql = "INSERT INTO %s (%s) VALUES (%s)" % (table, columns, values)
                cursor.execute(sql)

    def select(self, table, query="*", where=""):
        if self.connected:
            items = list()
            with self.connection.cursor() as cursor:
                sql = "select %s from %s" % (query, table)
                if where is not "":
                    sql += "where %s" % where
                cursor.execute(sql)
                for row in cursor:
                    items.append(row)
            return items

    def commit(self):
        if self.connected:
            self.connection.commit()
