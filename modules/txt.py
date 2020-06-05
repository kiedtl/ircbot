# random commands that involve
# simply piping text into a command
# and posting the result

import common, subprocess
from subprocess import Popen, PIPE, STDOUT

async def rev13(self, chan, src, msg):
    txt = ""
    try:
        txt = common.get_backlog_msg(self, chan, msg)[1]
    except:
        await self.message(chan, self.err_backlog_too_short)
        return

    res = common.run(self, ['caesar'], txt)
    await self.message(chan, res)

async def rot13(self, chan, src, msg):
    txt = ""
    try:
        txt = common.get_backlog_msg(self, chan, msg)[1]
    except:
        await self.message(chan, self.err_backlog_too_short)
        return

    res = common.run(self, ['rot13'], txt)
    await self.message(chan, res)

async def init(self):
    self.cmd['rev13'] = rev13
    self.cmd['rot13'] = rot13
    self.help['rot13'] = ['ebg13 grkg jvgu gur /ova/ebg13 hgvyvgl', '']
    self.help['rev13'] = ['attempt to decrypt rot13-encrypted messages', '']