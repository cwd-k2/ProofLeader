# -*- coding: utf-8 -*-
import re

# ．，を、。に変換
def correct_punctuation(text):
    text = re.sub("．", r"。", text)
    text = re.sub("，", r"、", text)
    return text


# 数字を三桁ごとに区切ってカンマ
def fancy_digits(num_str):
    numbers_before_comma = num_str.count(",")
    s = num_str.split(".")
    ret = re.sub(r"(\d)(?=(\d\d\d)+(?!\d))", r"\1,", s[0])

    if len(s) > 1:
        ret += "." + s[1]

    return ret, ret.count(",") - numbers_before_comma


# 前後に空白を入れる
def make_spaces(text):
    # 数値の前に空白
    text = re.sub(r"([^\n\d, \.])([+-]?(?:\d+\.?\d*|\.\d+))", r"\1 \2", text)
    # 数値の後ろに空白
    text = re.sub(r"([+-]?(?:\d+\.?\d*|\.\d+))([^\n\d, \.])", r"\1 \2", text)
    # 日本語 + 英字の間に空白
    text = re.sub(r"([亜-熙ぁ-んァ-ヶ]+)([a-zA-Z])", r"\1 \2", text)
    # 英字 + 日本語の間に空白
    text = re.sub(r"([a-zA-Z]+)([亜-熙ぁ-んァ-ヶ])", r"\1 \2", text)

    return text


def spacer(text):
    res_text = ""

    # テキスト変換から除外する箇所の開始, 終了のキーワードかな [(start, end)]
    # TODO: refactoring
    del_index = [m.span() for m in re.finditer("<pre>|</pre>|```|`|「|」{1}", text)]
    del_index.insert(0, (0, 0))
    del_index.append((len(text), len(text)))

    for i in range(len(del_index) - 1):
        # 除外する箇所の末尾と先頭に挟まれた箇所ってことかな
        sub_text = text[del_index[i][1] : del_index[i + 1][0]]

        if i % 2 == 0 or (  # 「英記号列(プログラム)」は除外
            del_index[i][1] > 0
            and text[del_index[i][1] - 1] == "「"
            and not re.fullmatch("[^亜-熙ぁ-んァ-ヶ]*", sub_text)
        ):
            sub_text = make_spaces(sub_text)
            num_poses = re.finditer(r"([+-]?(?:\d+\.?\d*|\.\d+))", sub_text)

            shift = 0  # カンマを置いた回数

            for p in num_poses:  # 三桁ごとにカンマ
                u, v = p.span()

                s, tmp_shift = fancy_digits(sub_text[u + shift : v + shift])

                sub_text = sub_text[0 : u + shift] + s + sub_text[v + shift :]

                shift += tmp_shift

            if i + 1 < len(del_index):
                res_text += sub_text + text[del_index[i + 1][0] : del_index[i + 1][1]]
            else:
                res_text += sub_text

        else:
            res_text += sub_text + text[del_index[i + 1][0] : del_index[i + 1][1]]

    return res_text


def converter(text):
    text = correct_punctuation(text)
    text = spacer(text)

    return text
