import sqlite3
from passlib.hash import pbkdf2_sha256

DATABASE_NAME = "app.db"

def create_connection():
    """Create a connection to the SQLite database specified by DATABASE_NAME.

    This function attempts to connect to the SQLite database file defined by
    the global DATABASE_NAME variable. If the connection is successful, it returns
    the connection object; otherwise, it prints the error and returns None.

    Returns:
    - conn (sqlite3.Connection or None): The connection object to the database
      if successful, or None if the connection could not be established.
    """
    conn = None
    try:
        conn = sqlite3.connect(DATABASE_NAME)
    except sqlite3.Error as e:
        print(e)
    return conn

def create_table(create_table_sql):
    """Create a table in the SQLite database using the provided SQL statement.

    This function connects to the SQLite database and executes a SQL statement
    to create a table. It uses `create_connection()` to get a database connection.
    After executing the create table SQL command, it commits the changes and
    closes the connection to the database.

    Parameters:
    - create_table_sql (str): A SQL statement for creating a table in the database.

    Notes:
    - The function handles exceptions internally, printing any errors encountered
      during the connection or table creation process.
    - It ensures that the database connection is closed properly in case of
      success or failure.
    """
    try:
        conn = create_connection()
        c = conn.cursor()
        c.execute(create_table_sql)
        conn.commit()
    finally:
        if conn:
            conn.close()

def create_users_table():
    """Creates the users table in the database if it does not already exist.

    This function is responsible for ensuring that the necessary table structure for
    storing user information is present in the database before the application starts
    processing any user-related operations.
    """
    sql_create_users_table = """ CREATE TABLE IF NOT EXISTS users (
                                        id integer PRIMARY KEY,
                                        username text NOT NULL UNIQUE,
                                        password_hash text NOT NULL,
                                        is_premium integer NOT NULL DEFAULT 0
                                    ); """
    create_table(sql_create_users_table)

def add_user(username, password, is_premium=False):
    """Adds a new user to the database.

    Parameters:
    - username (str): The username of the new user.
    - password (str): The password for the new user, which should be securely hashed.

    Returns:
    - bool: True if the user was successfully added, False otherwise.
    """
    conn = create_connection()
    with conn:
        password_hash = pbkdf2_sha256.hash(password)
        sql = ''' INSERT INTO users(username,password_hash,is_premium)
                  VALUES(?,?,?) '''
        cur = conn.cursor()
        cur.execute(sql, (username, password_hash, is_premium))
        conn.commit()
        return cur.lastrowid

def verify_user(username, password):
    """Verifies a user's login credentials.

    Parameters:
    - username (str): The username of the user attempting to log in.
    - password (str): The password provided by the user, to be checked against the stored hash.

    Returns:
    - tuple: (bool, bool) where the first bool indicates if the user is authenticated,
             and the second bool indicates if the user is a premium member.
    """
    conn = create_connection()
    with conn:
        cur = conn.cursor()
        cur.execute("SELECT password_hash, is_premium FROM users WHERE username = ?", (username,))
        row = cur.fetchone()
        if row:
            password_hash, is_premium = row
            if pbkdf2_sha256.verify(password, password_hash):
                return True, bool(is_premium)
    return False, False

