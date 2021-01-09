import os

from pathlib import Path

def search_markdowns(path):
    ex_list = []
    targets = []

    exclusion_list = search_upwards(path, 'exclusion_list.csv')

    if exclusion_list:
        with open(exclusion_list, mode='r') as f:
            ex_list = [Path(line.strip()).resolve() for line in f.readlines()]

    def recursive(path):  # dfs
        for target in path.iterdir():
            if target.is_dir():
                recursive(target)
            elif target.is_file() and target.match("*.md"):
                if not target in ex_list:
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

