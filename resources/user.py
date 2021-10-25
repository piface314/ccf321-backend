from flask import jsonify, g
from flask_restful import reqparse
import models as m
from time import time


class User:
    parser = reqparse.RequestParser()
    parser.add_argument('username', type=str, required=True, help="O campo 'username' não pode ser deixado em branco.")
    parser.add_argument('password', type=str, required=True, help="O campo 'password' não pode ser deixado em branco.")

    @staticmethod
    def verify_password(utoken, password, key):
        user, expiration = m.User.get_by_token(utoken, key)
        if expiration and time() > expiration:
            return False
        if not user:
            user = m.User.get(utoken)
            if not user or not user.check_password(password):
                return False
        g.user = user
        return True

    @staticmethod
    def login(key, duration=3600):
        token = g.user.get_token(key, duration)
        return jsonify({'token': token.decode('ascii'), 'duration': duration})

    @staticmethod
    def signup():
        data = User.parser.parse_args()
        if m.User.get(data['username']):
            return {'message': f"Usuário \"{data['username']}\" já existe."}, 403
        try:
            user = m.User(**data)
            user.add()
            return jsonify(user.as_dict()), 201
        except:
            return {'message': 'Um erro interno ocorreu ao cadastrar usuário.'}, 500
