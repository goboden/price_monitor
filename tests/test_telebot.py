from telebot import send_message
from telebot.secret import TEST_CHAT_ID


def test_send_mesage():
    send_message(chat_id=TEST_CHAT_ID, text='Oops!')
    assert True
