
import sqlite3
from sqlite3 import Error

import datetime
import json
import sys

# How we connect this REST API to Skluma codebase.
sys.path.append('db_files')

# Access user's config file, and get path to Skluma's SQLite DB from it.
try:
    with open("skluma_cfg.json") as f:
        skluma_cfg = json.load(f)
        DATABASE = skluma_cfg["db_path"]
        f.close()

except FileNotFoundError as e:
    print(e)


class SklumaDB:
    def __init__(self):
        self.connected_bool = False
        self.conn = None

        self.db_name = DATABASE

    def connect_to_db(self):

        if not self.connected_bool:
            try:
                self.conn = sqlite3.connect(self.db_name)
                self.connected_bool = True
                return self.conn

            except Error as e1:
                print(e1)
                return self.conn

    def insert_file(self, conn, query_string):
        if self.conn is not None:
            try:
                insert_into(conn, query_string)

            except Error as e2:
                print(e2)

    def close_db(self, conn):
        try:
            conn.close()
        except Error as e4:
            print("WARNING: "  + str(e4))
            pass
        return True


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

    print(query_string)

    try:
        cur = conn.cursor()
        cur.execute(query_string)
        conn.commit()
        return True

    except Error as e3:  # TODO: Find specific error-type.
        print("[ERROR] Failure with DB_UTILS.INSERT_INTO command...")
        print(e3)
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
