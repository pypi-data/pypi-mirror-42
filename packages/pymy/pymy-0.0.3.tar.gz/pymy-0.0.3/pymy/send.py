# -*- coding: utf-8 -*-
import pymysql

from . import create
from . import mysql_credentials


def send_to_mysql(
        instance,
        data,
        replace=True,
        batch_size=1000,
        types=None,
        primary_key=(),
        create_boolean=False):
    """
    data = {
        "table_name" 	: 'name_of_the_mysql_schema' + '.' + 'name_of_the_mysql_table' #Must already exist,
        "columns_name" 	: [first_column_name,second_column_name,...,last_column_name],
        "rows"		: [[first_raw_value,second_raw_value,...,last_raw_value],...]
    }
    """

    connection_kwargs = mysql_credentials.credential(instance)
    print("Initiate send_to_mysql...")

    print("Test to know if the table exists...")
    if (not create.existing_test(instance, data["table_name"])) or (types is not None) or (primary_key != ()):
        create_boolean = True

    print("Test to know if the table exists...OK")

    if create_boolean:
        create.create_table(instance, data, primary_key, types)

    con = pymysql.connect(**connection_kwargs)
    cursor = con.cursor()

    if replace:
        cleaning_request = '''DELETE FROM ''' + data["table_name"] + ''';'''
        print("Cleaning")
        cursor.execute(cleaning_request)
        print("Cleaning Done")

    boolean = True
    index = 0
    total_nb_batchs = len(data["rows"]) // batch_size + 1
    while boolean:
        temp_row = []
        for i in range(batch_size):
            if not data["rows"]:
                boolean = False
                continue
            temp_row.append(data["rows"].pop())

        final_data = []
        for x in temp_row:
            for y in x:
                final_data.append(y)

        temp_string = ','.join(map(lambda a: '(' + ','.join(map(lambda b: '%s', a)) + ')', tuple(temp_row)))

        inserting_request = '''INSERT INTO ''' + data["table_name"] + ''' (''' + ", ".join(
            data["columns_name"]) + ''') VALUES ''' + temp_string + ''';'''
        if final_data:
            cursor.execute(inserting_request, final_data)
        index = index + 1
        percent = round(index * 100 / total_nb_batchs, 2)
        if percent < 100:
            print("\r   %s / %s (%s %%)" % (str(index), total_nb_batchs, str(percent)), end='\r')
        else:
            print("\r   %s / %s (%s %%)" % (str(index), total_nb_batchs, str(percent)))
    con.commit()

    cursor.close()
    con.close()

    print("data sent to redshift")
    return 0

