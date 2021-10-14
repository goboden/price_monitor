import os

DB_NAME = 'price_monitor.db'
DB_URI = 'sqlite:///' + os.path.join(os.path.abspath(os.path.dirname(__file__)), DB_NAME)

SECRET_KEY = 'add your token'
LOG_FILENAME = "db_module.log"
PASSWORD_LENGHT = 11
