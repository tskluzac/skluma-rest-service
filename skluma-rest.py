
import globus_sdk
import json
import uuid
import sqs_queues


from flask import Flask, request, jsonify, Response
from mdf_forge.forge import Forge


app = Flask(__name__)

hardpath = "/home/tskluzac/Downloads/"


@app.route('/', methods=['GET'])
def hello():
    print("BANANAS!")
    return "Skluma is working! You've sent an empty request."


@app.route('/<file_uuid>', methods=['GET'])
def get_status(file_uuid):
    return "Status for file {}:".format(file_uuid)


# TODO (TYLER) for Wednesday.
@app.route('/process_file/<filename>', methods=['POST'])
def submit_file(filename):

    qualified_dns = "http://149.165.156.146"

    file_uuid = uuid.uuid5(uuid.NAMESPACE_DNS, qualified_dns)

    # TODO: Note, trying to 'transitively' use Globus auth via forge object from notebook.

    # TODO: 2.  Submit opened file for metadata extraction (QUEUES!).
    # TODO: Deal with duplicate names.
    full_path = hardpath + filename
    submit_response = sqs_queues.sqs_producer(full_path, str(file_uuid))
    print(submit_response)

    # TODO: 3. Save metadata to db. (in Skluma-local-deploy?)

    # TODO: 4. Give callback when it finishes.

    # Return response that the job is accepted and the job is started.
    return Response(json.dumps({'filepath_uuid': str(file_uuid), 'status':202}))


if __name__ == '__main__':
    app.run(debug=True)
