"""
WeHelp BootCamp Assignemt - Stage 2 -*- MySQL connect function -*-
Update date: 2022/12/27
Authored by SC Siao
"""

import mysql.connector
import mysql.connector.pooling

from dotenv import load_dotenv
import os
load_dotenv()
MySQL_password = os.getenv("MySQL_password")
MySQL_user = os.getenv("MySQL_user")


connector_pool = mysql.connector.pooling.MySQLConnectionPool(
	host = "localhost",
	user = MySQL_user,
	password = MySQL_password,
	database = "taipei_day_trip",
	pool_name = "mypool",
	pool_size = 5,
)

def query_data_read(sql_command):
    print(connector_pool)
    conn=connector_pool.get_connection()
    try:
        cursor=conn.cursor(dictionary=True)
        cursor.execute(sql_command)
        return cursor.fetchall()
    finally:
        conn.close()

def query_data(sql_command,input):
    print(connector_pool)
    conn=connector_pool.get_connection()
    try:
        cursor=conn.cursor(dictionary=True)
        cursor.execute(sql_command,input)
        return cursor.fetchall()
    finally:
        conn.close()

def insert_or_update_data(sql_command,input):
    print(connector_pool)
    conn=connector_pool.get_connection()
    try:
        cursor=conn.cursor(dictionary=True)
        cursor.execute(sql_command,input)
        conn.commit()
        return cursor.fetchall()
    finally:
        conn.close()
