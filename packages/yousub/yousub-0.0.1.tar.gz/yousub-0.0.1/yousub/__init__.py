import sys
from urllib.error import HTTPError, URLError

from .models import YouSub, NoSubtitleException
from .options import parse_options
from .models import logger

name = "yousub"
__version__ = '0.0.1'

def main():
    try:
        parser, args = parse_options()
        YouSub.run(url=args.url, dir=args.directory, show=args.show, lang=args.lang, filetype=args.filetype)
    except (HTTPError, URLError) as error:
        sys.exit('ERROR: No response, can you open this url in browser?')
    except NoSubtitleException as error:
        sys.exit(error.msg)
    except KeyboardInterrupt:
        sys.exit('Cancelled by user')


__all__ = ['main', ]
