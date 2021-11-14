import argparse
from backend.update_prices import update_urls

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Update prices.')
    parser.add_argument('--price-update', action='store_true', help='update prices for all goods')
    args = parser.parse_args()

    if args.price_update:
        update_urls()
