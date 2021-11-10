import argparse
from database import create_db, drop_db
from backend.update_prices import update_urls

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Create/Drop database.')
    parser.add_argument('--create', action='store_true', help='create database')
    parser.add_argument('--drop', action='store_true', help='drop database')
    parser.add_argument('--price-update', action='store_true', help='update prices for all goods')
    args = parser.parse_args()

    if args.create:
        create_db()
    if args.drop:
        drop_db()
    if args.price_update:
        update_urls()
