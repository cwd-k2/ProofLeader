# -*- coding: utf-8 -*-
import re
import os

class WordFinder:

    def __init__(self, path):
        self.list = []
        self.note = "> \033[1;36mWORD FOUND\033[0m line:{:3d}, col:{:3d}: \033[36m{}\033[0m"

        if not os.path.isfile(str(path)):
            return

        with open(str(path)) as f:
            self.list = [line.strip() for line in f.readlines()]

    def notate(self, text):
        notations = []

        for i, line in enumerate(text.splitlines()):

            for word in self.list:
                matched = re.search(word, line)

                if matched:
                    notations.append(
                            self.__notate_str(i + 1, matched.start(), word))

        return notations

    def __notate_str(self, line_num, where_is_it, word):
        return self.note.format(line_num, where_is_it, word)
