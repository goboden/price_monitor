from url_parser.parsers import Parser
from url_parser.exceptions import ParserNotFoundError, ParseError


def parse(url, no_cache=False, cache_ttl=None):
    try:
        parser = Parser.create(url)
        if no_cache:
            parser.use_cache = False
        if cache_ttl is not None:
            parser.cache.ttl = cache_ttl
        
        parser.parse()
        return parser.data
    except (ParserNotFoundError, ParseError) as e:
        # log()
        print(e)
        raise e