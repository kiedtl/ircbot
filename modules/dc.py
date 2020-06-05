import common, subprocess
from common import modname
from subprocess import Popen, PIPE, STDOUT

async def calc(self, chan, src, msg):
    res = common.run(self, ['dc'], ''.join(msg))
    if res == '':
        res = '(None)'
    lines = res.split('\n')
    for line in lines:
        await self.message(chan, '{} {}'
            .format(modname('dc'), line))

async def init(self):
    self.cmd['dc'] = calc
    self.help['dc'] = ['dc [num] - evaluate expression with /bin/dc (more)',
        'dc is a stack-based reverse-Polish notation calculator. See dc(1) for more information.']
