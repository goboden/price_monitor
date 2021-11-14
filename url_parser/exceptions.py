class BadURLError(Exception):
    def __init__(self, url_info):
        self.message = f'Bad URL {url_info}'
        super().__init__(self.message)


class ParserNotFoundError(Exception):
    def __init__(self, domain):
        self.message = f'Parser not found for {domain}'
        super().__init__(self.message)


class FetchError(Exception):
    pass


class ParseError(Exception):
    def __init__(self, info):
        self.message = f'Parse error: {info}'
        super().__init__(self.message)


class NotExistCacheError(Exception):
    pass


class TooOldCacheError(Exception):
    pass
