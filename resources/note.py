from flask import g, request
from flask_restful import Resource, reqparse
import models as m


class Notes(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('timestamp', type=str, required=True, help="O campo 'timestamp' não pode ser deixado em branco.")
    parser.add_argument('title', type=str, required=True, help="O campo 'title' não pode ser deixado em branco.")
    parser.add_argument('desc', type=str, required=True, help="O campo 'desc' não pode ser deixado em branco.")
    parser.add_argument('mood', type=int, required=True, help="O campo 'mood' não pode ser deixado em branco.")
    # parser.add_argument('colortag', type=list, required=True, help="O campo 'colortag' não pode ser deixado em branco.")

    def __init__(self, auth):
        self.__auth_get = auth.login_required(self.__get)
        self.__auth_post = auth.login_required(self.__post)
        super().__init__()

    def get(self):
        return self.__auth_get()

    def post(self):
        return self.__auth_post()

    def __get(self):
        username = g.user.username
        return {'notes': [note.as_dict() for note in m.Note.get_all(username)]}

    def __post(self):
        username = g.user.username
        args = Notes.parser.parse_args()
        try:
            args['colortag'] = request.json.get('colortag', [])
            note = m.Note(username=username, **args)
            note.add()
            return note.as_dict(), 200
        except:
            return {'message': "Um erro interno ocorreu ao tentar salvar sua anotação!"}, 500


class Note(Resource):
    k_args = {'timestamp', 'title', 'desc', 'mood', 'colortag'}

    def __init__(self, auth):
        self.__auth_get = auth.login_required(self.__get)
        self.__auth_put = auth.login_required(self.__put)
        self.__auth_delete = auth.login_required(self.__delete)
        super().__init__()

    def get(self, id):
        return self.__auth_get(id)

    def put(self, id):
        return self.__auth_put(id)

    def delete(self, id):
        return self.__auth_delete(id)

    def __get(self, id):
        username = g.user.username
        note = m.Note.get(id, username)
        if note:
            return note.as_dict()
        return {'message': "Anotação não encontrada."}, 404

    def __put(self, id):
        username = g.user.username
        note = m.Note.get(id, username)
        if note:
            try:
                args = {k: v for k, v in request.json.items() if Note.k_args}
                note.update(**args)
            except:
                return {'message': "Um erro interno ocorreu ao tentar salvar sua anotação!"}, 500
            return note.as_dict(), 200
        return {'message': "Anotação não encontrada."}, 404

    def __delete(self, id):
        username = g.user.username
        note = m.Note.get(id, username)
        if note:
            try:
                note.delete()
            except:
                return {'message': "Um erro interno ocorreu ao tentar deletar sua nota!"}, 500
            return {'message': 'Nota deletada com sucesso!'}, 200
        return {'message': "Anotação não encontrada."}, 404
