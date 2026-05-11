import sqlalchemy
from data.db_session import SqlAlchemyBase


class Level(SqlAlchemyBase):
    __tablename__ = 'levels'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=False, unique=True)   # easy, normal, hard, extreme
    points = sqlalchemy.Column(sqlalchemy.Integer, nullable=False)             # 50, 100, 150, 200