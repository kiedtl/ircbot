# random commands that involve
# simply piping text into a command
# and posting the result

import subprocess, common
from common     import modname
from subprocess import Popen, PIPE, STDOUT

async def list_mods(self, chan, src, msg):
    await self.message(chan, '{} loaded: {}'
        .format(modname('modules'), list(self.modules.keys())))

async def init(self):
    self.cmd['modules'] = list_mods
    self.help['modules'] = ['modules - list loaded modules']
