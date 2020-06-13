import subprocess
from subprocess import Popen, PIPE, STDOUT

def loadlogs(chan):
    logf = open('chans/{}.log'.format(chan))
    res = logf.read().split('\n')
    logf.close()
    return res

def nohighlight(nick):
    return nick[0] + '\u200c' + nick[1:]

def modname(name):
    """Get a stylized version of module name"""
    return '[\x032{}\x0f]'.format(name)

def get_backlog_msg(self, chan, msg):
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
    proc = Popen(cmd, stdout=PIPE,
        stderr=STDOUT, stdin=PIPE)
    out, err = proc.communicate(stdin.encode('utf-8'))
    print('stdin="{}"'.format(stdin.encode('utf-8')))
    exit = proc.wait()
    return out.decode('utf-8').rstrip()

async def init(self):
    self.err_backlog_too_short = 'error: backlog too short'
