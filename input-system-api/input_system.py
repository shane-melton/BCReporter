import pyodbc
import json
import sys


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
        con = pyodbc.connect(
            'Driver={{ODBC Driver 13 for SQL Server}};'
            'Server={};'
            'Database={};'
            'uid={};pwd={}'.format(self.host_location, self.db, self.username, self.password))
        return [con, True]

    def insert(self, table, columns, values):
        if self.connected:
            cur = self.connection.cursor()
            # EX: table="test", columns=["a", "b", "c"], values=["d", "e", "f"]
            # sql_command = INSERT INTO test(? ? ? ) VALUES(? ? ? )
            sql_command = "INSERT INTO " + table + "(" + columns[0]
            for col in columns[1:]:
                sql_command += ", " + col
            sql_command += ") VALUES(?" + ", ?"*(len(values)-1) + ")"

            sql_vals = values
            print(sql_command, file=sys.stderr)
            print(sql_vals, file=sys.stderr)
            cur.execute(sql_command, sql_vals)
            self.connection.commit()

    def select(self, table, query="*", lhs="", rhs=""):
        if self.connected:
            items = list()
            cur = self.connection.cursor()
            sql_command = "SELECT " + query + " FROM " + table
            sql_vals = []
            if lhs is not "":
                sql_command += " WHERE " + lhs + " = ?"
                sql_vals.append(rhs)
            print(sql_command, file=sys.stderr)
            print(sql_vals, file=sys.stderr)
            cur.execute(sql_command, sql_vals)
            for res in cur.fetchall():
                items.append(res)
            # result = cur.fetchone()
            # while result:
            #     print(result, file=sys.stderr)
            #     items.append(result)
            #     result = cur.fetchone()
            return items

    def create_table(self, table_name, columns, primary_key):
        if self.connected:
            cur = self.connection.cursor()
            sql_command = "CREATE TABLE ? (" + ("? ?,"*int(len(columns)/2)) + " PRIMARY KEY(?))"
            sql_vals = [table_name] + columns + [primary_key]
            try:
                cur.execute(sql_command, sql_vals)
            except:
                print("Command:")
                print(sql_command)
                print("Vals:")
                print(sql_vals)
            self.connection.commit()


class InputSystem:
    data_db = Database(_username="root", _password="password", _host_location="localhost\SQLEXPRESS", _db="data")
    system_db = Database(_username="root", _password="password", _host_location="localhost\SQLEXPRESS", _db="system")
    col_schema_table = "schemas"
    rule_table = "rules"
    # Will use only [1:] for inserts to skip "id"
    col_schema_columns = ["id", "schema__name", "schema__", "id_field"]
    rule_columns = ["id", "schema__", "rule_name", "rule_description", "rule__"]

    def __init__(self, data_db_login, system_db_login):
        self.data_db = Database(_username=data_db_login["username"], _password=data_db_login["password"],
                                _host_location=data_db_login["host"], _db=data_db_login["db_name"])
        self.system_db = Database(_username=system_db_login["username"], _password=system_db_login["password"],
                                  _host_location=system_db_login["host"], _db=system_db_login["db_name"])

    def __init__(self):
        pass

    def get_file_column_schema(self, schema_name):
        """
        Execute SELECT * FROM system_db.schemas WHERE schema_name=<schema_name>
        Finds and returns the column schema that corresponds to the input schema name
        :param schema_name:
        :return: { "schema_name": <string>, "schema": <json/string>, "id_field": <string> }
        """
        result = self.system_db.select(table=self.col_schema_table, lhs="schema__name", rhs=schema_name)
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
        columns = ["file_name", "TEXT"]
        for k, v in column_schema.items():
            columns.append(str(k))
            columns.append(str(v))
        self.data_db.create_table(schema_name, columns, primary_key)
        self.system_db.insert(self.col_schema_table, self.col_schema_columns[1:], [schema_name, json.dumps(column_schema), primary_key])

    def upload_file_data(self, file_name, file_data, file_schema_name, file_schema):
        """

        :param file_name: Name of the file that this data came from
        :param file_data: list of dictionaries, with dictionary keys matching with the keys in file_schema
        :param file_schema_name: Name of the file schema
        :param file_schema: ordered dictionary with dictionary keys matching the key structure of the internal db for this file_schema
        :return:
        """
        cols = ["file_name"] + file_schema.keys()
        for row in file_data:
            structured_row = [file_name] + [row[key] for key in file_schema.keys()]
            self.data_db.insert(table=file_schema_name, columns=cols, values=structured_row)

    def upload_rule(self, schema, rule_name, rule_description, rule):
        """

        :param schema:
        :param rule_name:
        :param rule_description:
        :param rule:
        :return:
        """
        values = [schema, rule_name, rule_description, rule]
        self.system_db.insert(self.rule_table, self.rule_columns[1:], values)

    def get_rule(self, rule_name):
        """

        :param rule_name:
        :return:
        """
        result = self.system_db.select(self.rule_table, "*", "rule_name={}".format(rule_name))
        return result
