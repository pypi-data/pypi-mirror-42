import json
from contextlib import contextmanager
from pathlib import Path
from os import environ

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.engine.url import URL

from dblist import base


def get_db_credentials():
    db_credentials_path = Path(environ['DBLIST_DB_CREDENTIALS_PATH'])
    with db_credentials_path.open() as handle:
        db_credentials = json.load(handle)
    return db_credentials


@contextmanager
def session_scope():
    """Provide a transactional scope around a series of operations."""
    session = Session()
    try:
        yield session
        session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()


engine_url = URL(**get_db_credentials())
engine = create_engine(engine_url, echo=False)
base.Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
