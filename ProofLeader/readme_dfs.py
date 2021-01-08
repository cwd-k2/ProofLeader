import pathlib
import os
import converter


def dfs(dir=""):
    f = open('./ProofLeader/exclusion_list.csv')
    exFiles = [line.strip() for line in f.readlines()]
    f.close()

    files = []

    def recursive(path):  # dfs
        for po in path.iterdir():
            if po.is_dir():
                recursive(po)
            elif po.is_file() & po.match("*.md"):
                if not str(po) in exFiles:
                    files.append(str(po))

    root = "./" + dir
    recursive(pathlib.Path(root))

    return files

    #  for file in files:
    #      converter.converter(file)
    #      print(file + " : \033[32mOK\033[0m")
    #
    #  print("converter : \033[32mALL OK\033[0m")
