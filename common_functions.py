import pyodbc
from sqlalchemy import create_engine
from urllib.parse import quote_plus
from config import azure_sql_db_credentials


def azure_sql_db_connection():
    db_username, db_password = azure_sql_db_credentials()

    server = 'nz-personal-nh.database.windows.net'
    database = 'general-data-collection'
    username = db_username
    password = db_password
    connection_url = 'DRIVER={ODBC Driver 17 for SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password
    connection = pyodbc.connect(connection_url)
    quoted = quote_plus(connection_url)
    sqlalchmey_engine = create_engine('mssql+pyodbc:///?odbc_connect={}'.format(quoted))  # , fast_executemany=True)


    return(connection, sqlalchmey_engine)

