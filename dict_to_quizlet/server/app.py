from flask import Flask, jsonify, request
from flask_cors import CORS


BOOKS = [
    {
        'title': 'On the Road',
        'author': 'Jack Kerouac',
        'read': True
    },
    {
        'title': 'Harry Potter and the Philosopher\'s Stone',
        'author': 'J. K. Rowling',
        'read': False
    },
    {
        'title': 'Green Eggs and Ham',
        'author': 'Dr. Seuss',
        'read': True
    }
]

# configuration
DEBUG = True

# instantiate the app
app = Flask(__name__)
app.config.from_object(__name__)

# enable CORS
CORS(app, resources={r'/*': {'origins': '*'}})


# sanity check route
@app.route('/ping', methods=['GET'])
def ping_pong():
    return jsonify('pong!')


@app.route('/books', methods=['GET', 'POST'])
def all_books():
    response_object = {"status": "success"}
    
    if request.method == "POST":
        post_data = request.get_json()
        BOOKS.append(post_data)
        response_object["message"] = "Books is added!"
    else:
        response_object["books"]  = BOOKS 

    return jsonify(response_object)


if __name__ == '__main__':
    app.run()
