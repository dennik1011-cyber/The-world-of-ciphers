import sqlalchemy as sa
import sqlalchemy.orm as orm
from sqlalchemy.orm import Session

SqlAlchemyBase = orm.declarative_base()

__factory = None


def global_init(db_file):
    global __factory

    if __factory:
        return

    if not db_file or not db_file.strip():
        raise Exception("Необходимо указать файл базы данных.")

    conn_str = f'sqlite:///{db_file.strip()}?check_same_thread=False'
    print(f"Подключение к базе данных по адресу {conn_str}")

    engine = sa.create_engine(conn_str, echo=False)
    __factory = orm.sessionmaker(bind=engine)

    from . import __all_models

    SqlAlchemyBase.metadata.create_all(engine)
    


def create_session() -> Session:
    global __factory
    return __factory()

def seed_database():
    session = db_session.create_session()

    if not session.query(Level).first():
        levels = [
            Level(id=1, name='easy', points=50),
            Level(id=2, name='normal', points=100),
            Level(id=3, name='medium', points=150),
            Level(id=4, name='hard', points=200),
        ]
        session.add_all(levels)

        ciphers = [
            Cipher(number=1, name='Шифр наоборот', level_id=1),
            Cipher(number=2, name='Шифр замены букв символами', level_id=1),
            Cipher(number=3, name='Каждая вторая буква', level_id=1),
            Cipher(number=4, name='Цифровой шифр', level_id=1),
            Cipher(number=5, name='Шифр первая буква', level_id=1),

            Cipher(number=6, name='Шифр Цезаря', level_id=2),
            Cipher(number=7, name='Шифр Атбаш', level_id=2),
            Cipher(number=8, name='Шифр Морзе', level_id=2),
            Cipher(number=9, name='Шифр Полибия', level_id=2),
            Cipher(number=10, name='Шифр Гронсфельда', level_id=2),

            Cipher(number=11, name='Шифр Виженера', level_id=3),
            Cipher(number=12, name='Шифр Плейфера', level_id=3),
            Cipher(number=13, name='Шифр четырёх квадратов', level_id=3),
            Cipher(number=14, name='Шифр Бэкона', level_id=3),
            Cipher(number=15, name='Шифр Трисемуса', level_id=3),

            Cipher(number=16, name='Шифр Rail Fence', level_id=4),
            Cipher(number=17, name='Шифр Колонной перестановки', level_id=4),
            Cipher(number=18, name='Шифр Вернама', level_id=4),
            Cipher(number=19, name='Шифр Гамильтона', level_id=4),
            Cipher(number=20, name='Двойной шифр', level_id=4),
        ]
        session.add_all(ciphers)
        session.commit()