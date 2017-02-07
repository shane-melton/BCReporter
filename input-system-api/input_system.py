import pyodbc


class InputSystem:
    data_db = Database(_username="admin", _password="password", _host_location="localhost", _db="data")
    system_db = Database(_username="admin", _password="password", _host_location="localhost", _db="system")
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

    def get_file_column_schema(self, schema_name):
        """
        Execute SELECT * FROM system_db.schemas WHERE schema_name=<schema_name>
        Finds and returns the column schema that corresponds to the input schema name
        :param schema_name:
        :return: { "schema_name": <string>, "schema": <json/string>, "id_field": <string> }
        """
        result = self.system_db.select(table=self.col_schema_table, where="id_field="+schema_name)
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
        for k, v in column_schema:
            columns.append(k)
            columns.append(v)
        self.data_db.create_table(schema_name, columns, primary_key)
        self.system_db.insert(self.col_schema_table, self.col_schema_columns[1:], [schema_name, column_schema, primary_key])

    def upload_file_date(self, file_name, file_data, file_schema_name, file_schema):
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
            con = pyodbc.connect(
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
