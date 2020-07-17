import uuid
from flask import Flask, jsonify, request
from flask_cors import CORS

from leo import LeoDict
from docs import list_docs, get_creds, get_folder_id, append_transalation, create_doc


# Instantiate the app
app = Flask(__name__)
app.config.from_object(__name__)
# Enabled to present the transalations in the same order as in Leo Dict
app.config["JSON_SORT_KEYS"] = False

# Enable CORS
CORS(app, resources={r"/*": {"origins": "*"}})

# Create dictionary object
ld = LeoDict()

# Sanity check route
@app.route("/ping", methods=["GET"])
def ping_pong():
    return jsonify("pong!")


@app.route("/translate/<query>", methods=["GET"])
def translate(query):
    response_object = {"status": "failure"}
    results = ld.search(query, "https://dict.leo.org/german-english/")
    response_object["translation"] = results

    response_object["status"] = "success"
    return jsonify(response_object)


@app.route("/docs/<folder>", methods=["GET", "POST"])
def docs(folder):
    response_object = {"status": "failure"}
    creds = get_creds()
    folder_id = get_folder_id(folder, creds)

    if request.method == "POST":
        payload = request.get_json()
        create_doc(payload.get("doc_name", ""), folder_id, creds)
        response_object["message"] = "Document is created!"

    elif request.method == "GET":
        response_object["docs"] = list_docs(folder_id, creds)

    response_object["status"] = "success"
    return jsonify(response_object)


@app.route("/append_translation/<doc_id>", methods=["POST"])
def append_translation(doc_id):
    response_object = {"status": "failure"}
    creds = get_creds()

    payload = request.get_json()
    append_transalation(
        payload.get("term", ""), payload.get("translation", ""), doc_id, creds
    )

    response_object["message"] = "Translation is appended!"

    response_object["status"] = "success"
    return jsonify(response_object)


if __name__ == "__main__":
    app.run()
