
import globus_sdk
import json
import uuid


from flask import Flask, request, jsonify, Response
from mdf_forge.forge import Forge


app = Flask(__name__)


@app.route('/', methods=['GET'])
def hello():
    return "Skluma is working! You've sent an empty request."


@app.route('/<file_uuid>', methods=['GET'])
def get_status(file_uuid):
    return "Status for file {}:".format(file_uuid)


# TODO (TYLER) for Tuesday.
@app.route('/<globus_endpoint>/<file_path>', methods=['POST'])
def submit_file(globus_endpoint, file_path):

    qualified_dns = "http://149.165.156.146"

    file_uuid = uuid.uuid5(uuid.NAMESPACE_DNS, qualified_dns)
    print(file_path + " " + str(file_uuid))

    # TODO: Note, trying to 'transitively' use Globus auth via forge object from notebook.

    # TODO: 1. Check whether endpoint exists.


    # TODO: 2. Check whether filename exists.
    # TODO: 2. Grab file from Globus and open.
    # TODO: 3. Submit opened file for metadata extraction.

    # Return response that the job is accepted and the job is started.
    return Response(json.dumps({'filepath_uuid': file_uuid}, status=202, mimetype='application/json'))







if __name__ == '__main__':
    app.run(debug=True)
