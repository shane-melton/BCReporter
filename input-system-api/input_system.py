import csv
import json
import pypyodc


class InputSystem:
    data_db = Database(_username="admin", _password="password", _host_location="localhost", _db="data")
    system_db = Database(_username="admin", _password="password", _host_location="localhost", _db="system")
    col_schema_table = "col_schemas"
    rule_table = "rules"
    file_col_table = "file_column"

    def __init__(self):
        pass

    def create_data_table(self, table_name, columns, primary_key):
        """
        Executes CREATE TABLE table_name(<columns>,PRIMARY KEY(primary_key)) on data_db
        :param table_name: string
        :param columns: list
        :param primary_key: string
        :return: True if created successfully, False otherwise
        """
        if not self.data_db.select(table_name):  # List is empty; table does not exist
            try:
                self.data_db.create_table(table_name, columns, primary_key)
                return True
            except:
                print("Error: Cannot create table " + table_name)
                return False
        print("Table " + table_name + " already exists")
        return False

    def get_file_column_schema(self, schema_name):
        """
        Execute SELECT * FROM system_db.schemas WHERE schema_name=<schema_name>
        Finds and returns the column schema that corresponds to the input schema name
        :param schema_name:
        :return: { "schema_name": <string>, "schema": <json/string>, "id_field": <string> }
        """
        result = self.system_db.select(table="schema", where="id_field="+schema_name)
        return result

    def upload_file_column_schema(self, schema_name, column_schema, primary_key):
        """
        Execute INSERT INTO system_db.schemas(schema_name, schema, id_field) VALUES
                                            (<schema_name>, <column_schema>, <primary_key>)
        Execute CREATE TABLE <schema_name>(<column_schema>, PRIMARY KEY(<primary_key>))
        Creates an entry in the system db that describes the new column schema.
        Creates a new table in the data db that follows the new column schema.
        :param schema_name:
        :param column_schema:
        :param primary_key:
        :return:
        """
        columns = []
        for k, v in column_schema:
            columns.append(k)
            columns.append(v)
        self.data_db.create_table(schema_name, columns, primary_key)
        self.system_db.insert("schemas", ["schema_name", "schema", "id_field"], [schema_name, column_schema, primary_key])

    def upload_file(self):
        pass

    def upload_rule(self, schema, rule_name, rule_description, rule):
        """

        :param schema:
        :param rule_name:
        :param rule_description:
        :param rule:
        :return:
        """
        columns = ["schema", "rule_name", "rule_description", "rule"]
        values = [schema, rule_name, rule_description, rule]
        self.system_db.insert("rules", columns, values)

    def get_rule(self, rule_name):
        """

        :param rule_name:
        :return:
        """
        result = self.system_db.select("rules", "*", "rule_name={}".format(rule_name))
        return result


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

    def __del__(self):
        if self.connected:
            self.connection.close()

    def connect(self):
        try:
            con = pypyodc.connect(
                'Driver={SQL Server};'
                'Server={};'
                'Database={};'
                'uid={};pwd={}'.format(self.host_location, self.db, self.username, self.password))
            return [con, True]
        except Exception as e:
            return [e, False]

    def insert(self, table, columns, values):
        if self.connected:
            cur = self.connection.cursor()
            # EX: table="test", columns=["a", "b", "c"], values=["d", "e", "f"]
            # sql_command = INSERT INTO test(? ? ? ) VALUES(? ? ? )
            sql_command = "INSERT INTO " + table + "(" + ("? "*len(columns)) + ") VALUES(" + ("? "*len(values)) + ")"
            sql_vals = columns + values
            cur.execute(sql_command, sql_vals)
            self.connection.commit()

    def select(self, table, query="*", where=""):
        if self.connected:
            items = list()
            cur = self.connection.cursor()
            sql_command = "SELECT ? FROM ?"
            sql_vals = [query, table]
            if where is not "":
                sql_command += " WHERE ?"
                sql_vals.append(where)
            cur.execute(sql_command, sql_vals)
            result = cur.fetchone()
            while result:
                items.append(result)
                result = cur.fetchone()
            return items

    def create_table(self, table_name, columns, primary_key):
        if self.connected:
            cur = self.conection.cursor()
            sql_command = "CREATE TABLE ? (" + ("? ? ,"*len(columns)) + " PRIMARY KEY(?))"
            sql_vals = [table_name] + columns + [primary_key]
            cur.execute(sql_command, sql_vals)
            self.connection.commit()
