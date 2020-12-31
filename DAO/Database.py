from config import POOL
import pymysql

def getConnect():
    conn = POOL.connection()
    cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
    return conn, cursor


def closeConnect(conn):
    conn.close()
