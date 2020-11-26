# random utility functions

import config
import subprocess
from subprocess import Popen, PIPE, STDOUT


class BacklogTooShort(Exception):
    pass


def get_backlog_msg(self, chan, msg):
    """get message from backlog"""

    if len(msg) < 1:
        msg = "1"
    try:
        back = int(msg) + 0
    except:
        back = 1

    if chan in self.backlog and len(self.backlog[chan]) >= back:
        return self.backlog[chan][0 - back]
    else:
        raise BacklogTooShort("backlog too short")


async def init(self):
