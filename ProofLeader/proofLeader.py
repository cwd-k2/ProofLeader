import sys
import os
import readme_dfs

from argparse import ArgumentParser

VERSION = '3.0.0-alpha_cwd-k2'

arg_parser = ArgumentParser()

arg_parser.add_argument(
        'file',
        nargs='*',
        help='ファイル/フォルダを指定して実行')
arg_parser.add_argument(
        '-v',
        '--version',
        help='show version and exit',
        action='store_true')

args = arg_parser.parse_args()

if args.version:
    print(VERSION)
    sys.exit(0)

for f in args.file:
    readme_dfs.dfs(f)

print("\033[32mCHECK!!\033[0m -> https://competent-morse-3888be.netlify.app/")

