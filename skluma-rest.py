
import db_utils
import json
import sys

from flask import Flask, request, Response, g


app = Flask(__name__)

# TODO: Move to skluma_cfg file.
hard_path = "/home/tskluzac/Downloads/"

# How we connect this REST API to Skluma codebase.
sys.path.append('db_files')

DATABASE = 'db_files/sklumadb4.db'


@app.route('/', methods=['GET', 'POST'])
def hello():
    print("BANANAS!")
    return "Skluma is working! You've sent an empty request."


@app.route('/<job_uuid>', methods=['GET'])
def get_job_status(job_uuid):
    return "Status for file {}:".format(job_uuid)


@app.route('/process_file', methods=['POST'])
def submit_file():

    file_data = json.loads(request.data)
    # Leave here to have an easily-accessible offline source of data.
    # file_data = {"task_id": "a", "job_id": "b", "file_path": "c", "uniq_path": "d"}

    task_id = file_data["task_id"]
    job_id = file_data["job_id"]
    file_path = file_data["file_path"]
    uniq_path = file_data["uniq_path"]

    # Get instance of SklumaDB class, connect to DB, and insert metadata.
    skluma_db = db_utils.SklumaDB()
    skluma_conn = skluma_db.connect_to_db()
    insert_success = skluma_db.insert_file(skluma_conn, db_utils.make_insert_string(task_id, job_id, file_path, uniq_path))

    if not insert_success:
        raise LookupError("[ERROR] Unable to add file.")

    return Response(json.dumps({"task_id": task_id, "job_id": job_id, "process": "SUBMITTED"}))


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


if __name__ == '__main__':
    app.run(debug=True, port=5001)
