from flask import Flask, jsonify, request, Response
from flask_pymongo import PyMongo
from werkzeug.security import generate_password_hash, check_password_hash
from bson import json_util
from bson.objectid import ObjectId


app = Flask(__name__)
app.config['MONGO_URI'] = 'mongodb://localhost:27017/flaskmongodb'
mongo = PyMongo(app)


def send_response(body):
    return Response(body, mimetype='application/json')


@app.route('/users', methods=['POST'])
def create_user():
    # Receiving data
    username = request.json['username']
    password = request.json['password']
    email = request.json['email']

    if username and email and password:
        hashed_password = generate_password_hash(password)
        id = mongo.db.users.insert_one(
            {
                'username': username,
                'password': hashed_password,
                'email': email,
            }
        )
        response = {
            'id': str(id.inserted_id),
            'username': username,
            'password': hashed_password,
            'email': email,
        }
        return response
    else:
        return not_found()


@app.route('/users', methods=['GET'])
def get_users():
    users = mongo.db.users.find()
    response = json_util.dumps(users)

    return send_response(response)


@app.route('/users/<id>', methods=['GET'])
def get_user(id):
    user = mongo.db.users.find_one({'_id': ObjectId(id)})
    response = json_util.dumps(user)

    return send_response(response)


@app.route('/users/<id>', methods=['PUT'])
def update_user(id):
    # Setup
    username = request.json['username']
    password = request.json['password']
    email = request.json['email']

    if username and email and password:
        hashed_password = generate_password_hash(password)
        mongo.db.users.update_one(
            {
                '_id': ObjectId(id)
            },
            {
               '$set': {
                    'username': username,
                    'password': hashed_password,
                    'email': email,
                }
            }
        )
        response = jsonify({
            'message': 'User with id = ' + id + ' was updated'
        })
    return response


@app.route('/users/<id>', methods=['DELETE'])
def delete_user(id):
    mongo.db.users.delete_one({'_id': ObjectId(id)})
    response = jsonify({
        'message': 'User with id(' + id + ') was deleted',
    })
    return response


@app.errorhandler(404)
def not_found(error=None):
    response = jsonify({
        'message': 'Resource not found: ' + request.url,
        'status': 404
    })
    response.status_code = 404

    return response


if __name__ == "__main__":
    app.run(debug=True)
