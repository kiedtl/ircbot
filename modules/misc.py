# random commands that involve
# simply piping text into a command
# and posting the result

import subprocess, common, random
from common import modname

async def list_mods(self, chan, src, msg):
    await self.message(chan, '{} loaded: {}'
        .format(modname('modules'), list(self.modules.keys())))

async def ping(self, chan, src, msg):
    await self.message(chan, '{} {}: {}'
        .format(modname('ping'), src,
            random.choice(['yes?', 'pong!', 'what?', 'hmmm?',
                'at your service!'])))

async def init(self):
    self.cmd['modules'] = list_mods
    self.cmd['ping'] = ping
    self.help['modules'] = ['modules - list loaded modules']
    self.help['ping'] = ['ping - check if I\'m responding']
