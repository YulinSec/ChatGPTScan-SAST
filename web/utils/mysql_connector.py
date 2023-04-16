import functools
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from utils.config import Config


class MysqlGlobal(object):
    __instance = None
    __engine = None

    def __new__(cls, *args, **kwargs):
        if not cls.__instance:
            cls.__instance = object.__new__(cls)
        return cls.__instance

    @classmethod
    def generate_engine(cls):
        if not MysqlGlobal.__engine:
            config = Config().config["db"]
            engine = create_engine(f'mysql+mysqlconnector://{config["username"]}:{config["password"]}@{config["ip"]}:{config["port"]}/{config["database"]}',
                                   pool_size=100,
                                   max_overflow=100,
                                   pool_recycle=2,
                                   echo=False)
            cls.__engine = engine

    @property
    def mysql_session(self):
        self.generate_engine()
        return sessionmaker(bind=MysqlGlobal.__engine)()


def mysql_session(method):
    @functools.wraps(method)
    def wrapper(*args, **kwargs):
        session = MysqlGlobal().mysql_session
        return method(*args, session, **kwargs)
    return wrapper

