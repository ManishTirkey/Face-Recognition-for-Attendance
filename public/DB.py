import mysql.connector
from public.DB_config import *


def ConnectDB(database=None):
    """
    creates a connection with the MySQL
    :param database:
    :return:
    """
    try:
        connection = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            database=database
        )

        # if connection.is_connected():
        # print("Connected to MySQL Database")
        return connection
    except mysql.connector.Error as err:
        raise err


def Connect(db_name=DB_NAME):
    return ConnectDB(db_name)


def Disconnect(conn, cursor=None) -> None:
    """
    Disconnects the connections
    :param cursor:
    :param conn:
    :return:
    """

    if 'conn' in locals() and conn.is_connected:
        # if conn.is_connected():
        try:
            if cursor is not None:
                cursor.close()
        except:
            ...

        finally:
            conn.close()


def Execute(connection, query, value=None):
    """
    Executes any queries
    :param value:
    :param connection:
    :param query:
    :return:
    """

    # Creating a cursor object
    cur = connection.cursor()

    try:
        cur.execute(query, value)
        connection.commit()
    except Exception as e:
        raise e
    else:
        return cur


def Execute_Fetch(connection, query, value=None):
    """
    Executes any queries for fetching the data
    :param value:
    :param connection:
    :param query:
    :return:
    """

    # Creating a cursor object
    cur = connection.cursor()

    try:
        cur.execute(query, value)
        return cur
    except Exception as e:
        raise e



