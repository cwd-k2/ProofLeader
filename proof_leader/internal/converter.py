# -*- coding: utf-8 -*-
import re

# ．，を、。に変換
def correct_punctuation(text):
    return re.sub("．", r"。", re.sub("，", r"、", text))


# 数字を三桁ごとに区切ってカンマ
def fancy_digits(num):
    beforeCommaNum = num.count(",")
    s = num.split(".")
    ret = re.sub(r"(\d)(?=(\d\d\d)+(?!\d))", r"\1,", s[0])
    if len(s) > 1:
        ret += "." + s[1]
    return ret, ret.count(",") - beforeCommaNum


# 前後に空白を入れる
def space(text):
    resText = ""
    delIndex = [m.span() for m in re.finditer("<pre>|</pre>|```|`|「|」{1}", text)]
    delIndex.insert(0, (0, 0))
    delIndex.append((len(text), len(text)))

    for i in range(len(delIndex) - 1):
        subText = text[delIndex[i][1] : delIndex[i + 1][0]]

        if i % 2 == 0 or (  # 「英記号列(プログラム)」は除外
            delIndex[i][1] > 0
            and text[delIndex[i][1] - 1] == "「"
            and not re.fullmatch("[^亜-熙ぁ-んァ-ヶ]*", subText)
        ):
            subText = re.sub(
                r"([^\n\d, \.])([+-]?(?:\d+\.?\d*|\.\d+))", r"\1 \2", subText
            )  # 数値の前に空白
            subText = re.sub(
                r"([+-]?(?:\d+\.?\d*|\.\d+))([^\n\d, \.])", r"\1 \2", subText
            )  # 数値の後ろに空白
            subText = re.sub(
                r"(\n[a-zA-Z]+)([亜-熙ぁ-んァ-ヶ])", r"\1 \2", subText
            )  # 先頭英字の後ろに空白

            numPoses = re.finditer(r"([+-]?(?:\d+\.?\d*|\.\d+))", subText)
            shift = 0  # カンマを置いた回数
            for p in numPoses:  # 三桁ごとにカンマ
                s, tmpShift = fancy_digits(
                    subText[p.span()[0] + shift : p.span()[1] + shift]
                )
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


def converter(text):
    text = correct_punctuation(text)
    text = space(text)

    return text
