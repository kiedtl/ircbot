import subprocess
from subprocess import Popen, PIPE, STDOUT

async def calc(self, c, n, m):
    if len(m) < 1:
        m = ["1"]
    try:
        back = int(m[0])+0
    except:
        back = 1

    ms = []
    if c in self.backlog and len(self.backlog[c]) >= back:
        ms = self.backlog[c][0-back]
    else:
        await self.message(c, 'error: my backlog is too short!')
        return

    dc = Popen(['dc'],
            stdout=PIPE, stderr=STDOUT, stdin=PIPE)
    (out, err) = dc.communicate(ms[1].encode('utf-8'))
    exit = dc.wait()

    res = out.decode('utf-8').rstrip()
    await self.message(c, res)

async def init(self):
    self.cmd['dc'] = calc
    self.help['dc'] = ['dc [num] - evaluate expression with /bin/dc (more)',
        'dc is a stack-based calculator. See dc(1) for more information.']
