
import json
import uuid
import sys
import datetime
import requests

from flask import Flask, request, jsonify, Response


app = Flask(__name__)

# TODO: Move to skluma_cfg file.
hard_path = "/home/tskluzac/Downloads/"

# How we connect this REST API to Skluma codebase.
sys.path.append('../skluma-local-deploy')


@app.route('/', methods=['GET', 'POST'])
def hello():
    print("BANANAS!")
    return "Skluma is working! You've sent an empty request."


@app.route('/<job_uuid>', methods=['GET'])
def get_job_status(job_uuid):
    return "Status for file {}:".format(job_uuid)


@app.route('/process_file', methods=['POST'])
def submit_file():

    file_data = request.data
    task_id = file_data["task_id"]
    job_id = file_data["job_id"]
    file_path = file_data["filepath"]
    uniq_path = file_data["uniq_path"]

    try:
        # Create file entry in database.
        init_query = "INSERT INTO sklumadb4 (task_id, job_id, cur_status, subm_time, real_path, req_path) " \
                     "VALUES ({0}, {1}, {2}, {3}, {4}, {5})".format(str(task_id), str(job_id), str('TRANSFER'), str(datetime.datetime.now()), file_path, uniq_path)

        print(init_query)

    except:
        return Response({"status": 503})

    # return "Bazinga!"
    return Response({"status": 202})


if __name__ == '__main__':
    app.run(debug=True, port=5001)
