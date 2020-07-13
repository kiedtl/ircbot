# caesar cipher in Python

from string import ascii_lowercase as lc, ascii_uppercase as uc

def rot(n):
    lookup = str.maketrans(lc + uc, lc[n:] + \
        lc[:n] + uc[n:] + uc[:n])
    return lambda s: s.translate(lookup)
