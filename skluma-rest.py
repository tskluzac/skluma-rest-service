
import datetime
import db_utils
import json
import sqlite3
import sys

from flask import Flask, request, Response, g
from sqlite3 import Error


app = Flask(__name__)

# TODO: Move to skluma_cfg file.
hard_path = "/home/tskluzac/Downloads/"

# How we connect this REST API to Skluma codebase.
sys.path.append('../skluma-local-deploy')
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
                db_utils.insert_into(self.conn, query_string)

            except:
                print(" [DEBUG] PUT DB ERROR HERE. ")




@app.route('/', methods=['GET', 'POST'])
def hello():
    print("BANANAS!")
    return "Skluma is working! You've sent an empty request."


@app.route('/<job_uuid>', methods=['GET'])
def get_job_status(job_uuid):
    return "Status for file {}:".format(job_uuid)


@app.route('/process_file', methods=['POST'])
def submit_file():

    skluma_db = SklumaDB(DATABASE)

    file_data = json.loads(request.data)

    task_id = file_data["task_id"]
    job_id = file_data["job_id"]
    file_path = file_data["file_path"]
    uniq_path = file_data["uniq_path"]

    try:

        # Create file entry in database.
        init_query = "INSERT INTO sklumadb4 (task_id, job_id, cur_status, subm_time, real_path, req_path) " \
                     "VALUES ({0}, {1}, {2}, {3}, {4}, {5});".format(str(task_id), str(job_id), str('TRANSFER'), str(datetime.datetime.now()), file_path, uniq_path)



    except:
        return Response('BAD')

    return Response(json.dumps({"task_id": task_id, "job_id": job_id, "process": "SUBMITTED"}))


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

if __name__ == '__main__':
    app.run(debug=True, port=5001)
