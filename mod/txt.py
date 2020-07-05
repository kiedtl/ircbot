# random commands that involve
# simply piping text into a command
# and posting the result

import config, common, out

async def cmd_with_args(self, chan, cmd, msg):
    # TODO: throttling, disable in certain channels
    cmd = cmd + msg.split(' ')
    res = common.run(cmd, msg)
    for line in res.split('\n'):
        await self.message(chan, line)

async def figlet(self, chan, src, msg):
    await cmd_with_args(self, chan, ['figlet'], msg)

async def toilet(self, chan, src, msg):
    await cmd_with_args(self, chan, ['toilet', '--irc'], msg)

async def cowsay(self, chan, src, msg):
    await cmd_with_args(self, chan, ['cowsay'], msg)

async def cowthink(self, chan, src, msg):
    await cmd_with_args(self, chan, ['cowthink'], msg)

async def communist(self, chan, src, msg):
    txt = msg.upper()
    await self.message(chan, f'\x038,5 ☭ {txt} ☭ \x0f')

async def rev13(self, chan, src, msg):
    txt = []
    try:
        txt = common.get_backlog_msg(self, chan, msg)
    except:
        await out.msg(self, 'rev13', chan,
            [self.err_backlog_too_short])
        return

    res = common.run(['caesar'], txt[1])
    await out.msg(self, 'rev13', chan, [f'<{txt[0]}> {res}'])

async def rot13(self, chan, src, msg):
    txt = []
    try:
        txt = common.get_backlog_msg(self, chan, msg)
    except:
        await out.msg(self, 'rot13', chan,
            [self.err_backlog_too_short])
        return

    res = common.run(['rot13'], txt[1])
    await out.msg(self, 'rev13', chan, [f'<{txt[0]}> {res}'])

async def init(self):
    self.cmd['cowsay']    = cowsay
    self.cmd['cowthink']  = cowthink
    self.cmd['figlet']    = figlet
    self.cmd['rev13']     = rev13
    self.cmd['rot13']     = rot13
    self.cmd['toilet']    = toilet

    self.cmd['communist'] = communist
    self.cmd['com']       = communist

    self.help['rot13']   = ['rot13 - ebg13 grkg jvgu gur /ova/ebg13 hgvyvgl']
    self.help['rev13']   = ['rev13 - attempt to decrypt rot13-encrypted messages']
    self.help['communist'] = ['communist|com - \x038,5 ☭ SEIZE THE MEANS OF CHAOS PRODUCTION ☭\x04']
    self.help['com'] = self.help['communist']
    self.help['figlet'] = ['figlet [args] - use /bin/figlet to generate ascii art']
    self.help['toilet'] = ['toilet [args] - use /bin/toilet to generate ascii art']
    self.help['cowsay'] = ['cow{say,think} [args] - use /bin/cow{say,think} to generate ascii art']
    self.help['cowthink'] = self.help['cowsay']
