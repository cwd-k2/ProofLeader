import sys
import os

from argparse import ArgumentParser
from pathlib  import Path

from .notifier import *
from .internal import *

VERSION = '3.0.0-alpha_cwd-k2'

def main():
    arg_parser = ArgumentParser()

    arg_parser.add_argument(
            'file',
            nargs='*',
            help='ファイル/フォルダを指定して実行 (無い場合はカレントディレクトリが指定される)')
    arg_parser.add_argument(
            '-v',
            '--version',
            action='store_true',
            help='show version and exit')
    arg_parser.add_argument(
            '-i',
            '--inplace',
            action='store_true',
            help='inplace edit file[s]')

    home = Path(os.environ['HOME'])
    here = Path(os.getcwd())
    args = arg_parser.parse_args()

    if args.version:
        print(VERSION)
        sys.exit(0)

    if len(args.file) == 0:
        args.file.append('.')

    if not (home in here.parents or here == home):
        print('Error: this program should be executed under $HOME. exit.', file=sys.stderr)
        sys.exit(1)

    for file_or_directory in args.file:
        path = Path(file_or_directory)
        if not path.exists:
            continue

        path = path.resolve()
        if not (home in path.parents or path == home):
            print('Error: specified file(s) should be under $HOME. skip.', file=sys.stderr)
            continue

        targets = search_markdowns(path)
        word_list = search_upwards(path, 'word_list.csv')
        find_list = search_upwards(path, 'find_list.csv')

        suggestion = Suggestion(word_list)
        wordfinder = WordFinder(find_list)

        for t in targets:
            f = open(t, mode='r')
            text = f.read()
            f.close()

            notations = []

            notations.extend(suggestion.notate(text))
            notations.extend(wordfinder.notate(text))

            if len(notations) > 0:
                print("\033[1m{}\033[0m:".format(t))
                for note in notations:
                    print(note)

            converted_text = converter(text)

            if args.inplace:
                with open(t, mode='w') as f:
                    f.write(converted_text)
                    print("\033[1m{}\033[0m: \033[32mrewritten\033[0m".format(t))

            elif text != converted_text:
                print("\033[1m{}\033[0m:".format(t))
                print(converted_text)

    print("\033[32mCHECK HERE\033[0m -> https://competent-morse-3888be.netlify.app/")

