# pig latin implementation

import random
import re


def _two_chars(s):
    if len(s) < 2:
        return s[0]
    else:
        return s[0] + s[1]


def _has_upper(s):
    has = False
    for ch in s:
        if ch.isupper():
            has = True
            break
    return has


def pigify(ms):
    # filter out ZWNJ's, which is sometimes output
    # by bots e.g. tildebot
    ms = ms.replace("\u200c", "")

    # split on every non-alphabetic character,
    # keeping the delimiters so that they can be
    # added back later
    data = re.split(r"([!-/:-@\[-`{-~\ 0-9]+)", ms)

    disyms = [
        "sh",
        "gl",
        "ch",
        "ph",
        "tr",
        "br",
        "fr",
        "bl",
        "gr",
        "st",
        "sl",
        "cl",
        "pl",
        "fl",
    ]

    # translation happens in-place
    for k in range(len(data)):
        i = data[k]

        if len(i) == 0:
            continue

        # actual translation
        if i[0] in ["a", "e", "i", "o", "u"]:
            data[k] = i + "way"
        elif _two_chars(i) in disyms:
            data[k] = i[2:] + i[:2] + "ay"
        elif i.isalpha() == False:
            data[k] = i
        else:
            data[k] = i[1:] + i[0] + "ay"

        # correct captalization
        # e.g. "You've" => "ouYay'evay" => "Ouyay'evay"
        if _has_upper(data[k]):
            data[k] = data[k].lower()
            data[k] = data[k][:1].upper() + data[k][1:]

    return "".join(data)


def pig_ascii():
    return random.choice(
        [
            "(･ั(00)･ั)",
            "(´·(oo)·`)",
            "(·(oo)·)",
            "(v -(··)-v)",
            "(> (··) <)",
            "(° (··) °)",
        ]
    )
