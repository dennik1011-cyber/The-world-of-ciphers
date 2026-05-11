import sqlalchemy
from data.db_session import SqlAlchemyBase


class Cipher(SqlAlchemyBase):
    __tablename__ = 'ciphers'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    number = sqlalchemy.Column(sqlalchemy.Integer, nullable=False, unique=True)   # 1-20
    name = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    level_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('levels.id'), nullable=False)

    level = sqlalchemy.orm.relationship('Level', backref='ciphers')