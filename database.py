users = []


class UserExistsError(Exception):
    pass


def add_user(user_name, telegram_id, chat_id):
    print(f'{user_name} ({telegram_id}) from {chat_id}')
    if telegram_id not in users:
        users.append(telegram_id)
    else:
        raise UserExistsError
