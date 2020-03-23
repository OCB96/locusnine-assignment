# coding=utf-8

from .entities.entity import Session, engine, Base
from .entities.user import User
from flask import Flask, jsonify, request, abort, make_response
from flask_cors import CORS

from .entities.entity import Session, engine, Base
from .entities.user import User, UserSchema

# generate database schema
Base.metadata.create_all(engine)

# start session
session = Session()

# check for existing data
users = session.query(User).all()

if len(users) <= 1:
    # create and persist dummy user
    python_user = User("Oishi Bhattacharyya", "oishib96@gmail.com", "Customer Executive", "8240792848", "Active", "HTTP Request Notttt")
    session.add(python_user)
    session.commit()
    session.close()

    # reload users
    users = session.query(User).all()

# show existing users
print('### Users:')
for user in users:
    print(f'({user.id}) {user.name} - {user.email} - {user.role_type} - {user.mobile_number} - {user.activity_status}')

# creating the Flask application
app = Flask(__name__)
CORS(app)

# if needed, generate database schema
Base.metadata.create_all(engine)


@app.route('/')
def index():
    return "Welcome to NOT a black page for a change \o/"


@app.route('/users', methods=['GET'])
def get_users():
    # fetching from the database
    session = Session()
    user_objects = session.query(User).all()

    # transforming into JSON-serializable objects
    schema = UserSchema(many=True)
    users = schema.dump(user_objects)

    # serializing as JSON
    session.close()
    return jsonify(users)


@app.route('/users/<int:user_id>', methods=['GET'])
def retrieve_user(user_id):

    # fetching from the database
    session = Session()
    user_object = session.query(User).filter(User.id == user_id)

    # transforming into JSON-serializable objects
    schema = UserSchema(many=True)
    user = schema.dump(user_object)

    # serializing as JSON
    session.close()
    return jsonify(user)


@app.route('/users', methods=['POST'])
def create_user():
    # mount user object
    posted_user = UserSchema().load(request.get_json())

    user = User(**posted_user, created_by="HTTP post request")

    # persist user
    session = Session()
    session.add(user)
    session.commit()

    # return created user
    new_user = UserSchema().dump(user)
    session.close()
    return jsonify(new_user = new_user)


#@app.route('/users/<int:user_id>', methods=['PUT', 'PATCH])
#def update_user():
#    # mount user object
#    posted_user = UserSchema().load(request.get_json())
#    user = User(**posted_user, created_by="HTTP post request")

    
#    user = session.query(User).filter(User.id == user_id).\
#       update({User.age: User.age - 10}, synchronize_session=False)

#    # persist user
#    session.commit()

#    # return updated user
#    new_user = UserSchema().dump(user)
#    session.close()
#    return jsonify(new_user = new_user)


@app.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):

    # deleting from the database
    session = Session()
    user = session.query(User).filter(User.id == user_id).\
        delete(synchronize_session=False)

    # persist user
    session.commit()

    # serializing response
    session.close()
    if user == 1:
       return jsonify("Success.")
    else:
        return jsonify("User not Found")


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

