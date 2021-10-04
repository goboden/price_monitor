import os
from sqlalchemy import create_engine
from models import User, Price, Goods, db


basedir = os.path.abspath(os.path.dirname(__file__))
engine = create_engine('sqlite:///' + os.path.join(basedir, 'price_monitor.db'), echo=True)
db.metadata.create_all(engine)
