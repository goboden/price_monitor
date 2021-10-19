import os
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker


db_url = os.environ.get('DB_URL')
if not db_url:
    raise RuntimeError('Environment variable DB_URL is not set')
engine = create_engine(db_url)
session = scoped_session(sessionmaker(bind=engine))
