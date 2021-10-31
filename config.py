import os

DB_URI = 'sqlite:///' + os.path.join(os.path.abspath(os.path.dirname(__file__)), 'price_monitor.db')
LOG_FILENAME = os.path.join(os.path.abspath(os.path.dirname(__file__)), "price_monitor.log")
PASSWORD_LENGHT = 11
SALT = 'add your salt'