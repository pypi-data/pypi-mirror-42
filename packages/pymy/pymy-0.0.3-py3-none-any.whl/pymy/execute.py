import pymysql

from . import mysql_credentials


def execute_query(instance, query):
    connection_kwargs = mysql_credentials.credential(instance)
    connection_kwargs["cursorclass"] = pymysql.cursors.DictCursor
    connection = pymysql.connect(**connection_kwargs)

    cursor = connection.cursor()
    cursor.execute(query)
    connection.commit()
    result = cursor.fetchall()
    cursor.close()
    connection.close()
    return result
