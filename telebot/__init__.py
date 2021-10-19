from telegram.update import Update
from telegram.ext.callbackcontext import CallbackContext
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from telebot.secret import API_KEY
from url_parser import parse
from url_parser.exceptions import BadURLError, ParserNotFoundError
from url_parser.exceptions import ParseError, FetchError
import database
from database.exceptions import TelegramUserExistsError

bot_updater = Updater(API_KEY, use_context=True)
bot = bot_updater.bot


def send_message(chat_id, text):
    bot.send_message(chat_id=chat_id, text=text)


def start_handler(update: Update, context: CallbackContext):
    telegram_id = update.message.from_user.id
    user_name = update.message.from_user.name
    chat_id = update.message.chat.id
    try:
        database.add_user(user_name, telegram_id, chat_id)
        update.message.reply_text('Вы успешно зарегистрировались')
    # except database.UserExistsError:
    except TelegramUserExistsError:
        update.message.reply_text('Вы уже ранее регистрировались')


def password_handler(update: Update, context: CallbackContext):
    telegram_id = update.message.from_user.id
    password = database.generate_password(telegram_id)
    update.message.reply_text(f'Ваш новый пароль: {password}')


def add_url(update: Update, context: CallbackContext):
    url = update.message.text
    telegram_id = update.message.from_user.id
    try:
        parsed_data = parse(url)
        database.add_url(telegram_id, url, parsed_data.price)
        update.message.reply_text('Адрес успешно добавлен.')
    except BadURLError:
        update.message.reply_text('Вы ввели некорректный адрес.')
    except ParserNotFoundError:
        update.message.reply_text('Этот магазин пока не поддерживается.')
    except (ParseError, FetchError):
        update.message.reply_text('Что-то пошло не так ...')


dp = bot_updater.dispatcher
dp.add_handler(CommandHandler('start', start_handler))
dp.add_handler(CommandHandler('password', password_handler))
dp.add_handler(MessageHandler(Filters.text, add_url))