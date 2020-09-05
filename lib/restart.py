import os
import psutil
import sys


def restart():
    """
    Restarts the current program, with file objects and descriptors
    cleanup
    """

    p = psutil.Process(os.getpid())
    for handler in p.open_files() + p.connections():
        os.close(handler.fd)

    python = sys.executable
    os.execl(python, python, *sys.argv)
