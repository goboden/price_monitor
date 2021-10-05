import os
from sqlalchemy.orm import sessionmaker
from models import db, User, Goods, Price
from sqlalchemy import create_engine


def main():
    basedir = os.path.abspath(os.path.dirname(__file__))
    engine = create_engine('sqlite:///' + os.path.join(basedir, 'price_monitor.db'), echo=True)

    db.metadata.create_all(engine)

    Session = sessionmaker(bind=engine)
    session = Session()


if __name__ == "__main__":
    main()
