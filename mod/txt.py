# random commands that involve
# simply piping text into a command
# and posting the result

import config, common
from common import modname

async def communist(self, chan, src, msg):
    txt = msg.upper()
    await common.msg(self, chan,
        '\x038,5 ☭ {} ☭ \x0f'.format(txt))

async def rev13(self, chan, src, msg):
    txt = []
    try:
        txt = common.get_backlog_msg(self, chan, msg)
    except:
        await common.msg(self, chan,
            self.err_backlog_too_short)
        return

    res = common.run(self, ['caesar'], txt[1])
    await common.msg(self, chan, '<{}> {}'
        .format(txt[0], res))

async def rot13(self, chan, src, msg):
    txt = []
    try:
        txt = common.get_backlog_msg(self, chan, msg)
    except:
        await common.msg(self, chan,
            self.err_backlog_too_short)
        return

    res = common.run(self, ['rot13'], txt[1])
    await common.msg(self, chan, '<{}> {}'
        .format(txt[0], res))

async def init(self):
    self.cmd['rev13']   = rev13
    self.cmd['rot13']   = rot13

    self.cmd['communist'] = communist
    self.cmd['c'] = communist

    self.help['rot13']   = ['rot13 - ebg13 grkg jvgu gur /ova/ebg13 hgvyvgl']
    self.help['rev13']   = ['rev13 - attempt to decrypt rot13-encrypted messages']
    self.help['communist'] = ['communist - \x038,5 ☭ SEIZE THE MEANS OF CHAOS PRODUCTION ☭\x04']
    self.help['c'] = self.help['communist']
