
class ParserNotFoundError(Exception):
    def __init__(self, domain):
        self.message = f'Не найден модуль парсера для {domain}'
        super().__init__(self.message)


class ParseError(Exception):
    def __init__(self, info):
        self.message = f'Parse error: {info}'
        super().__init__(self.message)
