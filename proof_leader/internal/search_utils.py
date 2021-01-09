import os
import re

from pathlib import Path

def search_markdowns(path):
    ex_list = []
    targets = []

    exclusion_list = search_upwards(path, 'exclusion_list.csv')

    if exclusion_list:
        with open(exclusion_list, mode='r') as f:
            ex_list = [line.strip() for line in f.readlines()]

    def recursive(path):  # dfs
        for target in path.iterdir():

            if target.is_dir() and not regex_included(ex_list, str(target)):
                recursive(target)

            elif target.is_file() and target.match("*.md"):
                if not regex_included(ex_list, str(target)):
                    targets.append(target)

    recursive(path)

    return targets

def search_upwards(path, filename):
    if path.is_dir() and (path / filename).exists():
        return path / filename

    for parent in path.parents:
        if (parent / filename).exists():
            return parent / filename

        if parent == Path(os.environ['HOME']):
            return None

def regex_included(regex_list, target):
    for regex in regex_list:
        if re.match(regex, target):
            return True

    return False
