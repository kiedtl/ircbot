# :modules, :who, and :ping etc commands
import common, irc, random

async def list_mods(self, chan, src, msg):
    mods = ', '.join(sorted(list(self.modules.keys())))
    await irc.msg('modules', chan, [f'loaded: {mods}'])

async def status(self, chan, src, msg):
    res = common.run(['bin/sysinfo'], '')
    await irc.msg('status', chan, [f'~team status: {res}'])

async def ping(self, chan, src, msg):
    res = random.choice(['you rang?', 'yes?', 'pong!',
        'what?', 'hmmm?', 'at your service!'])
    await irc.msg('ping', chan, [f'{src}: {res}'])

async def whoami(self, chan, src, msg):
    await irc.msg('who', chan, [f'I\'m {self.nickname}, kiedtl\'s bot.'])
    await irc.msg('who', chan, ['https://github.com/kiedtl/ircbot'])
    await irc.msg('who', chan, 
        ['raves and rants: kiedtl‍＠‍tilde.team'])
    await irc.msg('who', chan, ['for usage info, try :help'])

async def init(self):
    self.cmd['modules'] = list_mods
    self.cmd['ping'] = ping
    self.cmd['who'] = whoami
    self.cmd['sysinfo'] = status

    self.help['modules'] = ['modules - list loaded modules']
    self.help['ping'] = ['ping - check if I\'m responding']
    self.help['who'] = ['who - get information about my owner']
    self.help['sysinfo'] = ['sysinfo - retrieve info for the tilde.team server']
