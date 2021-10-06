from sqlalchemy.orm import sessionmaker
from db_module.models import db
from sqlalchemy import create_engine
from config import DB_URI


def main():
    engine = create_engine(DB_URI, echo=True)

    db.metadata.create_all(engine)

    Session = sessionmaker(bind=engine)
    session = Session()


if __name__ == "__main__":
    main()
