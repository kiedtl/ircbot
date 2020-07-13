import common, irc
modname = 'fortune'

async def fortune(self, chan, src, msg):
    fort = common.run(['fortune', '-s'], '')
    await irc.msg(modname, chan, [fort])

async def init(self):
    self.cmd['fortune'] = fortune
    self.help['fortune'] = ['fortune - get a fortune']
