# :modules, :who, and :ping etc commands
import common, out, random

async def list_mods(self, chan, src, msg):
    mods = ', '.join(sorted(list(self.modules.keys())))
    await out.msg(self, 'modules', chan, [f'loaded: {mods}'])

async def status(self, chan, src, msg):
    res = common.run(['bin/sysinfo'], '')
    await out.msg(self, 'status', chan, [f'~team status: {res}'])

async def ping(self, chan, src, msg):
    res = random.choice(['you rang?', 'yes?', 'pong!',
        'what?', 'hmmm?', 'at your service!'])
    await out.msg(self, 'ping', chan, [f'{src}: {res}'])

async def whoami(self, chan, src, msg):
    await out.msg(self, 'who', chan, [f'I\'m {self.nickname}, kiedtl\'s bot.'])
    await out.msg(self, 'who', chan, ['https://github.com/kiedtl/ircbot'])
    await out.msg(self, 'who', chan, 
        ['raves and rants: kiedtl‍＠‍tilde.team'])
    await out.msg(self, 'who', chan, ['for usage info, try :help'])

async def init(self):
    self.handle_cmd['modules'] = list_mods
    self.handle_cmd['ping'] = ping
    self.handle_cmd['who'] = whoami
    self.handle_cmd['sysinfo'] = status

    self.help['modules'] = ['modules - list loaded modules']
    self.help['ping'] = ['ping - check if I\'m responding']
    self.help['who'] = ['who - get information about my owner']
    self.help['sysinfo'] = ['sysinfo - retrieve info for the tilde.team server']
