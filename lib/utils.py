def enum(**items):
    return type("Enum", (), items)

def flatten(src):
    """
    Flatten a list of lists
    """
    return [item for sublist in src for item in sublist]
