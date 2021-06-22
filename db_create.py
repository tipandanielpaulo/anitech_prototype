"""
This code is used to create an SQLite database to store DHT22 sensor data.

Columns: Id, Date, Temperature, and Humidity
"""

import sqlite3 # Import SQL Library
from sqlite3 import Error # Catch Errors

def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)

    return conn


def create_table(conn, create_table_sql):
    """ create a table from the create_table_sql statement
    :param conn: Connection object
    :param create_table_sql: a CREATE TABLE statement
    :return:
    """
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)


def main():
    database = "database.db"

    sql_create_projects_table = """ CREATE TABLE IF NOT EXISTS users (
                                        id integer PRIMARY KEY,
                                        username text NOT NULL,
                                        input_date text,
                                        email text
                                    ); """

    sql_create_tasks_table = """CREATE TABLE IF NOT EXISTS rq_sensor (
                                    id integer PRIMARY KEY,
                                    date text NOT NULL,
                                    temp float NOT NULL,
                                    humi float NOT NULL,
                                    co2x float NOT NULL,
                                    o2xx float NOT NULL
                                );"""

    # create a database connection
    conn = create_connection(database)

    # create tables
    if conn is not None:
        # create projects table
        create_table(conn, sql_create_projects_table)

        # create tasks table
        create_table(conn, sql_create_tasks_table)
    else:
        print("Error! cannot create the database connection.")


if __name__ == '__main__':
    main()
