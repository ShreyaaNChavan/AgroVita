import os

os.add_dll_directory('C:\\Users\\admin\\ShreyaProjects\\IBM\\.venv\\Lib\\site-packages\\clidriver\\bin')

import ibm_db

# Connection parameters
dsn_hostname = "6667d8e9-9d4d-4ccb-ba32-21da3bb5aafc.c1ogj3sd0tgtu0lqde00.databases.appdomain.cloud"
dsn_uid = "pwb07217"
dsn_pwd = "XXQDmfXomoWnzF9f"
dsn_driver = "{IBM DB2 ODBC DRIVER}"
dsn_database = "bludb"
dsn_port = "30367"
dsn_protocol = "TCPIP"
dsn_security = "SSL"

# DSN string for connection
dsn = (
    "DRIVER={0};"
    "DATABASE={1};"
    "HOSTNAME={2};"
    "PORT={3};"
    "PROTOCOL={4};"
    "UID={5};"
    "PWD={6};"
    "SECURITY={7};"
).format(dsn_driver, dsn_database, dsn_hostname, dsn_port, dsn_protocol, dsn_uid, dsn_pwd, dsn_security)

def get_db_connection():
    """Establishes and returns a database connection."""
    try:
        conn = ibm_db.connect(dsn, "", "")
        print("Connected to database:", dsn_database, "as user:", dsn_uid, "on host:", dsn_hostname)
        return conn
    except Exception as e:
        print("Unable to connect:", ibm_db.conn_errormsg())
        return None
