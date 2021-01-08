# -*- coding: utf-8 -*-
import re
import os
import read_file as File

class Warnings:

    def __init__(self, path):
        self.dict = {}
        self.note = "\033[33mWARNING\033[0m: {}:{}: ({}) => ({})"

        if not os.path.isfile(path):
            return

        f = open(path)

        for line in f:
            elems = line.strip().split(',')
            right = elems.pop(0)
            for wrong in elems:
                self.dict[wrong] = right

        f.close()

    def warn(self, text):

        for i, line in enumerate(text.splitlines()):

            for wrong, right in self.dict.items():
                matched = re.search(wrong, line)

                if matched:
                    print(self.note.format(line_num, matched.start(), matched.group(), right))




# ．，を、。に変換
def dotComma(text):
    return re.sub("．", r"。", re.sub("，", r"、", text))


# word_listを参照して警告
def word2Word(text, file, search):

    # if not os.path.isfile("./ProofLeader/word_list.csv"):
    #     return text

    # wordList = File.readFile("./ProofLeader/word_list.csv", True)

    warnings = Warnings('./ProofLeader/word_list.csv')
    warnings.warn(text)

    # find_listを開く
    if search:
        findListPath = "./ProofLeader/find_list.csv"
        if not os.path.isfile(findListPath):
            search = False
        with open(findListPath) as f:
            findList = [s.strip() for s in f.readlines()]

    textArr = text.splitlines()
    # wordOut = []
    findOut = []
    for i, text in enumerate(textArr):

        #  for li in wordList:  # 文字列警告
        #      reObj = re.search(li[0], text)
        #      if reObj:
        #          wordOut.append([i + 1, reObj.start(), reObj.group(), li[1]])

        if search:  # 文字列探索
            for li in findList:
                reObj = re.search(li, text)
                if reObj:
                    findOut.append([i + 1, reObj.start(), li])

    #  for c in wordOut:
    #      print("\033[33mWARNING\033[0m: {}:{}:{}: ({}) => ({})".format(file, c[0], c[1], c[2], c[3]))

    for c in findOut:
        print("\033[36mFOUND!!\033[0m: {}:{}:{}: ({})".format(file, c[0], c[1], c[2]))

    return "\n".join(textArr)


# 数字を三桁ごとに区切ってカンマ
def comma(num):
    beforeCommaNum = num.count(",")
    s = num.split(".")
    ret = re.sub("(\d)(?=(\d\d\d)+(?!\d))", r"\1,", s[0])
    if len(s) > 1:
        ret += "." + s[1]
    return ret, ret.count(",") - beforeCommaNum


# 前後に空白を入れる
def space(text):
    resText = ""
    delIndex = [m.span() for m in re.finditer("<pre>|</pre>|```|`|「|」{1}", text)]
    delIndex.insert(0, [0, 0])
    delIndex.append([len(text), len(text)])

    for i in range(len(delIndex) - 1):
        subText = text[delIndex[i][1] : delIndex[i + 1][0]]

        if i % 2 == 0 or (  # 「英記号列(プログラム)」は除外
            delIndex[i][1] > 0
            and text[delIndex[i][1] - 1] == "「"
            and not re.fullmatch("[^亜-熙ぁ-んァ-ヶ]*", subText)
        ):
            subText = re.sub(
                "([^\n\d, \.])([+-]?(?:\d+\.?\d*|\.\d+))", r"\1 \2", subText
            )  # 数値の前に空白
            subText = re.sub(
                "([+-]?(?:\d+\.?\d*|\.\d+))([^\n\d, \.])", r"\1 \2", subText
            )  # 数値の後ろに空白
            subText = re.sub(
                "(\n[a-zA-Z]+)([亜-熙ぁ-んァ-ヶ])", r"\1 \2", subText
            )  # 先頭英字の後ろに空白

            numPoses = re.finditer("([+-]?(?:\d+\.?\d*|\.\d+))", subText)
            shift = 0  # カンマを置いた回数
            for p in numPoses:  # 三桁ごとにカンマ
                s, tmpShift = comma(subText[p.span()[0] + shift : p.span()[1] + shift])
                subText = (
                    subText[0 : p.span()[0] + shift]
                    + s
                    + subText[p.span()[1] + shift :]
                )
                shift += tmpShift
            if i + 1 < len(delIndex):
                resText += subText + text[delIndex[i + 1][0] : delIndex[i + 1][1]]
            else:
                resText += subText
        else:
            resText += subText + text[delIndex[i + 1][0] : delIndex[i + 1][1]]
    return resText


def converter(file, search):
    text = File.readFile(file)

    text = dotComma(text)
    text = space(text)
    text = word2Word(text, file, search)

    with open(file, mode="w") as f:
        f.write(text)
