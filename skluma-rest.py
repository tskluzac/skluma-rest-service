
from flask import Flask, request
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
    # TODO: 1. Check whether endpoint exists.
    # TODO: 2. Check whether filename exists.
    # TODO: 2. Grab file from Globus and open.
    # TODO: 3. Submit opened file for metadata extraction.
    print("wow.")








if __name__ == '__main__':
    app.run()
