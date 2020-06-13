import common, subprocess
from common import modname
from subprocess import Popen, PIPE, STDOUT

async def do_calc(self, chan, msg, cmd):
    res = common.run(self, cmd, msg)
    if res == '':
        res = '(None)'
    lines = res.split('\n')
    for line in res.split('\n'):
        await self.message(chan, '{} {}'
            .format(modname('calc'), line))

async def dc_calc(self, chan, src, msg):
    await do_calc(self, chan, msg, ['dc'])

async def bc_calc(self, chan, src, msg):
    msg = msg + '\n' # bc complains if no newline
    await do_calc(self, chan, msg, ['bc', '-ql'])

async def init(self):
    self.cmd['dc'] = dc_calc
    self.cmd['bc'] = bc_calc
    self.help['dc'] = ['dc [expr] - evaluate expression with /bin/dc (more)',
        'dc is a reverse-Polish notation calculator. See dc(1) for details.']
