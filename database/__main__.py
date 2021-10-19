import argparse
from database.models import Base
from database import engine


def create_database():
    Base.metadata.create_all(engine)
    print(f'Database created: {engine.url}')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Databese module.',
                                     prog='database')
    parser.add_argument('--create',
                        action='store_true', help='creates database')
    args = parser.parse_args()

    if args.create:
        create_database()
