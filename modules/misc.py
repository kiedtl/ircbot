# :modules, :who, and :ping commands

import subprocess, common, random
from common import modname

async def list_mods(self, chan, src, msg):
    await self.message(chan, '{} loaded: {}'
        .format(modname('modules'), list(self.modules.keys())))

async def status(self, chan, src, msg):
    res = common.run(self, ['bin/sysinfo'], '')
    await common.msg(self, chan, '{} ~team status: {}'
        .format(modname('status'), res))

async def ping(self, chan, src, msg):
    await self.message(chan, '{} {}: {}'
        .format(modname('ping'), src,
            random.choice(['yes?', 'pong!', 'what?', 'hmmm?',
                'at your service!'])))

async def whoami(self, chan, src, msg):
    await self.message(chan, '{} I\'m k, kiedtl\'s bot.'
        .format(modname('who')))
    await self.message(chan, '{} https://github.com/kiedtl/ircbot'
        .format(modname('who')))
    await self.message(chan, '{} raves and rants: kiedtl [at] tilde.team'
        .format(modname('who')))
    await self.message(chan, '{} for usage info, try :help'
        .format(modname('who')))

async def init(self):
    self.cmd['modules'] = list_mods
    self.cmd['ping'] = ping
    self.cmd['who'] = whoami
    self.cmd['sysinfo'] = status

    self.help['modules'] = ['modules - list loaded modules']
    self.help['ping'] = ['ping - check if I\'m responding']
    self.help['who'] = ['who - get information about my owner']
    self.help['sysinfo'] = ['sysinfo - retrieve info for the tilde.team server']
