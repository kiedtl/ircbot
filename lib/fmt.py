# IRC formatting :D

RESET = "\x0f"

# --- attributes ---
def bold(x):
    return "\x02" + str(x) + RESET


def italic(x):
    return "\x1d" + str(x) + RESET


def underline(x):
    return "\x1f" + str(x) + RESET


# --- colors ---
def white(x):
    return "\x0300" + str(x) + RESET


def black(x):
    return "\x0301" + str(x) + RESET


def blue(x):
    return "\x0302" + str(x) + RESET


def green(x):
    return "\x0303" + str(x) + RESET


def lightred(x):
    return "\x0304" + str(x) + RESET


def red(x):
    return "\x0305" + str(x) + RESET


def magenta(x):
    return "\x0306" + str(x) + RESET


def brown(x):
    return "\x0307" + str(x) + RESET


def yellow(x):
    return "\x0308" + str(x) + RESET


def lightgreen(x):
    return "\x0309" + str(x) + RESET


def cyan(x):
    return "\x0310" + str(x) + RESET


def lightcyan(x):
    return "\x0311" + str(x) + RESET


def lightblue(x):
    return "\x0312" + str(x) + RESET


def lightmagenta(x):
    return "\x0313" + str(x) + RESET


def darkgray(x):
    return "\x0314" + str(x) + RESET


def gray(x):
    return "\x0315" + str(x) + RESET
