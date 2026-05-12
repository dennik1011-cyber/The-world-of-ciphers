import sqlalchemy
import datetime
from data.db_session import SqlAlchemyBase


class CompletedCipher(SqlAlchemyBase):
    __tablename__ = 'completed_ciphers'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    user_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('users.id'), nullable=False)
    cipher_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('ciphers.id'), nullable=False)
    solved_at = sqlalchemy.Column(sqlalchemy.DateTime, default=datetime.datetime.now)

    user = sqlalchemy.orm.relationship('User', backref='completed_ciphers')
    cipher = sqlalchemy.orm.relationship('Cipher', backref='completions')
