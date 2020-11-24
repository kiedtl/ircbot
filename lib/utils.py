def enum(**items):
    return type("Enum", (), items)


def flatten(src):
    """
    Flatten a list of lists
    """
    return [item for sublist in src for item in sublist]


def dedup(src):
    """
    Dedup an array.
    TODO: use binary search to speed this thing up...?
    """
    dest = []
    for i in src:
        if i not in dest:
            dest.append(i)
    return dest
