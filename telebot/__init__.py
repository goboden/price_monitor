from telegram.update import Update
from telegram.ext.callbackcontext import CallbackContext
from telegram.ext import Updater, CommandHandler
from telebot.secret import API_KEY


# bot = telegram.Bot(API_KEY)
# bot_updater = Updater(bot=bot, use_context=True)
bot_updater = Updater(API_KEY, use_context=True)
bot = bot_updater.bot


def send_message(chat_id, text):
    bot.send_message(chat_id=chat_id, text=text)


def start_handler(update: Update, context: CallbackContext):
    telegram_id = update.message.from_user.id
    user_name = update.message.from_user.name
    chat_id = update.message.chat.id
    update.message.reply_text(f'{user_name} ({telegram_id}) from {chat_id}')


dp = bot_updater.dispatcher
dp.add_handler(CommandHandler('start', start_handler))
