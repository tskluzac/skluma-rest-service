
import globus_sdk
import json
import uuid
import sqs_queues
import sys
import requests

from flask import Flask, request, jsonify, Response
from mdf_forge.forge import Forge


app = Flask(__name__)

# TODO: Move to skluma_cfg file.
hard_path = "/home/tskluzac/Downloads/"

# How we connect this REST API to Skluma codebase.
sys.path.append('../skluma-local-deploy')


@app.route('/', methods=['GET'])
def hello():
    print("BANANAS!")
    return "Skluma is working! You've sent an empty request."


@app.route('/<file_uuid>', methods=['GET'])
def get_status(file_uuid):
    return "Status for file {}:".format(file_uuid)


# TODO (TYLER) for Wednesday.
@app.route('/process_file/<filename>', methods=['POST', 'GET'])
def submit_file(filename):

    # TODO: Move to skluma_cfg file.
    qualified_dns = "http://149.165.156.146"

    file_uuid = uuid.uuid5(uuid.NAMESPACE_DNS, qualified_dns)

    # TODO: Note, trying to 'transitively' use Globus auth via forge object from notebook.

    full_path = hard_path + filename      # TODO: Deal with duplicate names (notebook side)

    thing = requests.get('http://127.0.0.1:5000/' + filename).content
    print(thing)

    # TODO: 3. Save metadata to db. (in Skluma-local-deploy?)

    # TODO: 4. Give callback when it finishes.

    # Return response that the job is accepted and the job is started.
    return Response(json.dumps({'filepath_uuid': str(file_uuid), 'status': 202}))


if __name__ == '__main__':
    app.run(debug=True, port=5001)
