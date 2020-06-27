# random utility functions

import config
import subprocess
from subprocess import Popen, PIPE, STDOUT

def loadlogs(chan):
    logf = open('irc/{}.log'.format(chan))
    res = logf.read().split('\n')
    logf.close()
    return res

def nohighlight(nick):
    """add a ZWNJ to nick to prevent highlight"""
    return nick[0] + '\u200c' + nick[1:]

def modname(name):
    """Get a stylized version of module name"""
    return '[\x032{}\x0f]'.format(name)

def get_backlog_msg(self, chan, msg):
    """get message from backlog"""

    if len(msg) < 1:
        msg = '1'
    try:
        back = int(msg) + 0
    except:
        back = 1

    if chan in self.backlog and len(self.backlog[chan]) >= back:
        return self.backlog[chan][0-back]
    else:
        raise Exception('backlog too short')

def run(self, cmd, stdin):
    """run command and return it's output"""
    proc = Popen(cmd, stdout=PIPE,
        stderr=STDOUT, stdin=PIPE)
    out, err = proc.communicate(stdin.encode('utf-8'))
    exit = proc.wait()
    return out.decode('utf-8').rstrip()

async def msg(self, chan, txt):
    await self.message(chan, txt)

async def init(self):
    self.err_backlog_too_short = 'error: backlog too short'
    self.err_invalid_logfile   = 'error: could not open log file'
    self.err_invalid_command   = 'error: invalid command'