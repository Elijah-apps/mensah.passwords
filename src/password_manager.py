import sqlite3
from sqlite3 import Error

db_file = 'passwords.db'

def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(e)
    return conn

def create_table(conn, create_table_sql):
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)

def add_password(conn, password_entry):
    sql = ''' INSERT INTO passwords(name, username, password)
              VALUES(?,?,?) '''
    cur = conn.cursor()
    cur.execute(sql, password_entry)
    conn.commit()
    return cur.lastrowid

def fetch_passwords(conn):
    cur = conn.cursor()
    cur.execute("SELECT * FROM passwords")
    return cur.fetchall()

def delete_password(conn, id):
    sql = 'DELETE FROM passwords WHERE id=?'
    cur = conn.cursor()
    cur.execute(sql, (id,))
    conn.commit()
