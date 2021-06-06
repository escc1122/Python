from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm.session import sessionmaker

host = ""
user = ""
dbname = ""
password = ""

db_string = "postgresql+psycopg2://{0}:{1}@{2}:5432/{3}".format(user, password, host, dbname)
engine = create_engine(db_string, echo=True)


def get_engine():
    return engine
