import argparse
from telebot import bot_updater


def start_bot():
    print('Bot started')
    bot_updater.start_polling()
    bot_updater.idle()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Telegram bot.',
                                     prog='telebot')
    parser.add_argument('--start', action='store_true', help='starts bot')
    args = parser.parse_args()

    if args.start:
        start_bot()
