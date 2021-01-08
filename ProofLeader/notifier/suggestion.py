# -*- coding: utf-8 -*-
import re
import os

class Suggestion:

    def __init__(self, path):
        self.dict = {}
        self.note = "> \033[1;33mSUGGESTION\033[0m line:{:3d}, col:{:3d}: \033[33m{}\033[0m => \033[34m{}\033[0m"

        if not os.path.isfile(str(path)):
            return

        f = open(str(path))

        for line in f:
            elems = line.strip().split(',')
            right = elems.pop(0)
            for wrong in elems:
                self.dict[wrong] = right

        f.close()

    def notate(self, text):
        notations = []

        for i, line in enumerate(text.splitlines()):

            for wrong, right in self.dict.items():
                matched = re.search(wrong, line)

                if matched:
                    notations.append(
                            self.__notate_str(
                                i + 1, matched.start(), matched.group(), right))

        return notations

    def __notate_str(self, line_num, where_is_it, what_is_it, right):
        return self.note.format(line_num, where_is_it, what_is_it, right)

