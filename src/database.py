from password_manager import create_connection, create_table, db_file

def init_db():
    conn = create_connection(db_file)
    if conn is not None:
        create_table_sql = """ CREATE TABLE IF NOT EXISTS passwords (
                                            id integer PRIMARY KEY,
                                            name text NOT NULL,
                                            username text NOT NULL,
                                            password text NOT NULL
                                        ); """
        create_table(conn, create_table_sql)
    else:
        print("Error! cannot create the database connection.")
