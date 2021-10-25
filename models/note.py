from db import db
from datetime import datetime


class Note(db.Model):

    __tablename__ = 'note'

    id = db.Column('id', db.Integer(), nullable=False, primary_key=True, autoincrement=True)
    username = db.Column('username', db.VARCHAR(length=64), nullable=False)
    timestamp = db.Column('timestamp', db.TIMESTAMP(), nullable=False)
    title = db.Column('title', db.VARCHAR(length=64), nullable=False)
    desc = db.Column('desc', db.TEXT(length=2048), nullable=False)
    mood = db.Column('mood', db.Integer(), nullable=False)
    colortag = db.Column('colortag', db.Integer(), nullable=False, default=0)

    date_fmt = '%Y-%m-%dT%H:%M:%S.%fZ'

    @staticmethod
    def __encode_colortag(colors):
        return sum(2 ** c for c in colors)

    @classmethod
    def get(cls, id, username):
        return cls.query.filter_by(id=id, username=username).first()

    @classmethod
    def get_all(cls, username):
        return cls.query.filter_by(username=username).all()


    def __init__(self, username, timestamp, title, desc, mood, colortag, id=None):
        self.id = id
        self.username = username
        self.timestamp = timestamp
        self.title = title
        self.desc = desc
        self.mood = mood
        self.colortag = colortag

    def __decode_colortag(self):
        tag = self.colortag
        return [i for i in range(tag.bit_length()) if (tag >> i) & 1]

    def as_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'timestamp': self.timestamp.strftime(Note.date_fmt),
            'title': self.title,
            'desc': self.desc,
            'mood': self.mood,
            'colortag': self.__decode_colortag()
        }

    def __setattr__(self, name, value):
        if name == 'timestamp':
            self.__dict__[name] = datetime.strptime(value, Note.date_fmt)
        elif name == 'colortag':
            self.__dict__[name] = Note.__encode_colortag(value)
        else:
            super().__setattr__(name, value)

    def add(self):
        db.session.add(self)
        db.session.commit()

    def update(self, **kwargs):
        for k, v in kwargs.items():
            if v is not None:
                setattr(self, k, v)
        self.add()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
