# IRC formatting :D

RESET = '\x0f'

# --- attributes ---
def bold(x):
    return '\x02' + x + RESET

def italic(x):
    return '\x1d' + x + RESET

def underline(x):
    return '\x1f' + x + RESET

# --- colors ---
def white(x):
    return '\x0300' + x + RESET

def black(x):
    return '\x0301' + x + RESET

def blue(x):
    return '\x0302' + x + RESET

def green(x):
    return '\x0303' + x + RESET

def lightred(x):
    return '\x0304' + x + RESET

def red(x):
    return '\x0305' + x + RESET

def magenta(x):
    return '\x0306' + x + RESET

def brown(x):
    return '\x0307' + x + RESET

def yellow(x):
    return '\x0308' + x + RESET

def lightgreen(x):
    return '\x0309' + x + RESET

def cyan(x):
    return '\x0310' + x + RESET

def lightcyan(x):
    return '\x0311' + x + RESET

def lightblue(x):
    return '\x0312' + x + RESET

def lightmagenta(x):
    return '\x0313' + x + RESET

def darkgray(x):
    return '\x0314' + x + RESET

def gray(x):
    return '\x0315' + x + RESET
