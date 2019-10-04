import sqlite3
from sqlite3 import Error


def create_connection(db_file):
    """ create a database connection to a SQLite db 
        specified by db_file 
    :param db_file: database file name
    :return: connection object or none
    """

    conn = None
    try:
        conn = sqlite3.connect(db_file)
        print(sqlite3.version)
    except Error as e:
        print(e)

    return conn

def create_table(conn, table_format):
    """ create a table from the passed table format
        and database connection
    :param conn: connection object
    :param table_format: a CREATE TABLE string
    """
    try:
        c = conn.cursor()
        c.execute(table_format)
    except Error as e:
        print(e)

def main():
    db_file = 'radio_ams.db'

    callsign_table = """ CREATE TABLE IF NOT EXISTS users (
                            callsign TEXT UNIQUE PRIMARY KEY,
                            last_date TEXT
                         ); """

    message_table = """ CREATE TABLE IF NOT EXISTS messages (
                            recipient TEXT,
                            m_id TEXT,
                            sender TEXT,
                            date TEXT,
                            subject TEXT,
                            body TEXT,
                            read INTEGER
                        ); """

    conn = create_connection(db_file)

    if conn is not None:
        create_table(conn, callsign_table)
        create_table(conn, message_table)
    else:
        print("Error creating database connection.")


if __name__ == '__main__':
    main()

