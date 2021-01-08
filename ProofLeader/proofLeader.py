import sys
import os
import readme_dfs
import converter

from argparse import ArgumentParser
from notifier import *

VERSION = '3.0.0-alpha_cwd-k2'

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

args = arg_parser.parse_args()

if args.version:
    print(VERSION)
    sys.exit(0)

if len(args.file) == 0:
    args.file.append('.')

for file_or_directory in args.file:
    targets = readme_dfs.dfs(file_or_directory)

    for t in targets:
        f = open(t, mode='r')
        text = f.read()
        f.close()

        notations = []

        i = Suggestion('./ProofLeader/word_list.csv')
        notations.extend(i.notate(text))

        w = WordFinder('./ProofLeader/find_list.csv')
        notations.extend(w.notate(text))

        if len(notations) > 0:
            print("\033[1m{}\033[0m:".format(t))
            for note in notations:
                print(note)

        converted_text = converter.converter(text)

        if args.inplace:
            with open(t, mode='w') as f:
                f.write(converted_text)
        elif text != converted_text:
            print(converted_text)

print("\033[32mCHECK HERE\033[0m -> https://competent-morse-3888be.netlify.app/")

