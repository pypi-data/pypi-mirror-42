import os
import argparse
from urllib import parse


def parse_options():
    parser = argparse.ArgumentParser()
    parser.add_argument("url", help="YouTube video url")
    parser.add_argument("-d", "--directory",
                        help="specify the output directory, if not exists then create automatically")
    parser.add_argument("-s", "--show",
                        help="only show available languages of subtitle, not downloading files",
                        action="store_true")
    parser.add_argument("-l", "--lang",
                        help="specify the language code")
    parser.add_argument("-f", "--filetype", help="xml, srt and json format, default: srt",
                        choices=['srt', 'xml', 'json'])
    args = parser.parse_args()
    args.directory = args.directory or os.getcwd()
    if not os.path.exists(args.directory):
        os.mkdir(args.directory)

    args.filetype = args.filetype or 'srt'
    args.url = parse.parse_qs(parse.urlparse(args.url).query)['v'][0]
    return parser, args
