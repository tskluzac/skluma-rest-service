
import sqlite3
from sqlite3 import Error

import datetime
import sys

sys.path.append('db_files')
DATABASE = 'sklumadb4.db'


class SklumaDB:
    def __init__(self, db_name):
        self.connected_bool = False
        self.conn = None

        self.db_name = db_name

    def connect_to_db(self, db_name):

        if not self.connected_bool:
            try:
                self.conn = sqlite3.connect(db_name)
                self.connected_bool = True
                return self.conn

            except Error as e:
                print(e)
                return self.conn

    def insert_file(self, query_string):
        if self.conn is not None:
            try:
                insert_into(self.conn, query_string)

            except:
                print(" [DEBUG] PUT DB ERROR HERE. ")


def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by the db_file
    :param db_file: database file
    :return: Connection object or None
    """
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)

    return None


def select_all_files(conn):
    """
    Query all rows in the tasks table
    :param conn: the Connection object
    :return:
    """
    cur = conn.cursor()
    cur.execute("SELECT * FROM files")

    rows = cur.fetchall()

    for row in rows:
        print(row)


def insert_into(conn, query_string):

    try:
        cur = conn.cursor()
        cur.execute(query_string)
        conn.commit()
        return True

    except:  # TODO: Find specific error-type.
        print("[ERROR] Failure with DB_UTILS.INSERT_INTO command...")
        return False


def db_str(in_string):
    return "'" + str(in_string) + "'"


def close_db(conn):
    conn.close()


def make_insert_string(task_id, job_id, file_path, uniq_path):
    init_query = "INSERT INTO files (task_id, job_id, cur_status, subtime, real_path, req_path) " \
                 "VALUES ({0}, {1}, {2}, {3}, {4}, {5});".format(db_str(task_id), db_str(job_id), db_str('TRANSFER'),
                                                                 db_str(datetime.datetime.now()), db_str(file_path),
                                                                 db_str(uniq_path))
    return init_query
