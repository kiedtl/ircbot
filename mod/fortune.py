import common, out
modname = 'fortune'

async def fortune(self, chan, src, msg):
    fort = common.run(['fortune', '-s'], '')
    await out.msg(self, modname, chan, [fort])

async def init(self):
    self.handle_cmd['fortune'] = fortune
    self.help['fortune'] = ['fortune - get a fortune']
