from subprocess import Popen, PIPE, STDOUT


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


def command(cmd: list, stdin: str):
    """
    A quick utility function to run a command, pass some stuff
    to its standard input, and return the command's output, ignoring
    the exit code.
    """
    proc = Popen(cmd, stdout=PIPE, stderr=STDOUT, stdin=PIPE)
    out, err = proc.communicate(stdin.encode("utf-8"))
    exit = proc.wait()
    return out.decode("utf-8")
