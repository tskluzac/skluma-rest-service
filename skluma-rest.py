
import json
import uuid
import sys
import requests

from flask import Flask, request, jsonify, Response


app = Flask(__name__)

# TODO: Move to skluma_cfg file.
hard_path = "/home/tskluzac/Downloads/"

# How we connect this REST API to Skluma codebase.
sys.path.append('../skluma-local-deploy')


@app.route('/', methods=['GET'])
def hello():
    print("BANANAS!")
    return "Skluma is working! You've sent an empty request."


@app.route('/<job_uuid>', methods=['GET'])
def get_job_status(job_uuid):
    return "Status for file {}:".format(job_uuid)


@app.route('/process_file/<filename>', methods=['POST', 'GET'])
def submit_file(filename):

    # TODO: Move to skluma_cfg file.
    qualified_dns = "http://149.165.156.146"

    job_uuid = uuid.uuid5(uuid.NAMESPACE_DNS, qualified_dns)


    full_path = hard_path + filename      # TODO: Deal with duplicate names (notebook side)
    final_metadata = requests.get('http://127.0.0.1:5000/' + filename).content

    # TODO: 3. Save metadata to db. (in Skluma-local-deploy?)

    # new_metadata = json.loads(thing)
    # new_metadata['filepath_uuid'] = str(file_uuid)
    # new_metadata['status'] = 202

    # TODO: Return response that the job is accepted and the job is started.
    return Response(json.dumps(new_metadata))


if __name__ == '__main__':
    app.run(debug=True, port=5001)
