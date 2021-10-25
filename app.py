from db import db
from flask import Flask, jsonify, g
from flask_httpauth import HTTPBasicAuth
from flask_restful import Api
import resources as res
import os

app = Flask(__name__)
key = os.urandom(12)
app.config['SECRET_KEY'] = key
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True

api = Api(app)
db.init_app(app)
auth = HTTPBasicAuth()

api.add_resource(res.Notes, '/notes', resource_class_args=(auth,))
api.add_resource(res.Note, '/notes/<int:id>', resource_class_args=(auth,))


@auth.verify_password
def verify_password(utoken, password):
    return res.User.verify_password(utoken, password, key)

@app.route('/login')
@auth.login_required
def login():
    return res.User.login(key, duration=3600)

@app.route('/signup', methods=['POST'])
def signup():
    return res.User.signup()


if __name__ == '__main__':
    if not os.path.exists('db.sqlite'):
        with app.app_context():
            db.create_all()
    app.run(host="192.168.1.7", debug=True)
