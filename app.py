from db import db
from flask import Flask
from flask_httpauth import HTTPBasicAuth
from flask_restful import Api
import resources as res
import os
from sys import argv


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

@app.after_request
def add_cors_headers_after(response):
    response.headers.add('Access-Control-Allow-Credentials', 'true')
    response.headers.add("Access-Control-Allow-Origin", "*")
    response.headers.add('Access-Control-Allow-Headers', "*")
    response.headers.add('Access-Control-Allow-Methods', "*")
    return response


if __name__ == '__main__':
    if len(argv) < 2:
        print("Especifique o host da API")
        exit(1)
    if not os.path.exists('db.sqlite'):
        with app.app_context():
            db.create_all()
    app.run(host=argv[1])
