# simple text manipulation stuff

# REQUIRE exe qrencode
# REQUIRE exe figlet
# REQUIRE exe toilet
# REQUIRE exe cowsay
# REQUIRE exe cowthink

import caesar
import config
import common
import out

async def cmd_with_args(self, chan, cmd, msg):
    # TODO: throttling, disable in certain channels
    cmd = cmd + msg.split(' ')
    res = common.run(cmd, msg)
    for line in res.split('\n'):
        await self.message(chan, line)

async def qrenco(self, chan, src, msg):
    await cmd_with_args(self, chan,
        ['qrencode', '-o', '-', '-t', 'UTF8'], msg)

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

async def rot13(self, chan, src, msg):
    res = caesar.rot(13)(msg)
    await out.msg(self, 'caesar', chan, [f'{res}'])

async def rot_n(self, chan, src, msg):
    args = msg.split(' ', 1)
    if len(args) < 2:
        await out.msg(self, 'caesar', chan,
            ['need rot number and message'])
        return

    try:
        rotn = int(args[0])
    except:
        await out.msg(self, 'caesar', chan,
            ['need rot number and message'])
        return

    res = caesar.rot(rotn)(args[1])
    await out.msg(self, 'caesar', chan, [f'{res}'])

async def init(self):
    self.handle_cmd['cowsay']    = cowsay
    self.handle_cmd['cowthink']  = cowthink
    self.handle_cmd['figlet']    = figlet
    self.handle_cmd['rot']       = rot_n
    self.handle_cmd['rot13']     = rot13
    self.handle_cmd['toilet']    = toilet
    self.handle_cmd['qr']        = qrenco
    self.handle_cmd['communist'] = communist

    self.aliases['communist'] = ['com', 'co']

    self.help['rot13']   = ['rot13 [message] - ebg13 grkg jvgu gur /ova/ebg13 hgvyvgl']
    self.help['rot']     = ['rot [rotation] [message] - shift letters in message']
    self.help['communist'] = ['communist - \x038,5 ☭ SEIZE THE MEANS OF CHAOS PRODUCTION ☭\x04']
    self.help['figlet'] = ['figlet [args] - use /bin/figlet to generate ascii art']
    self.help['toilet'] = ['toilet [args] - use /bin/toilet to generate ascii art']
    self.help['cowsay'] = ['cow{say,think} [args] - use /bin/cow{say,think} to generate ascii art']
    self.help['cowthink'] = self.help['cowsay']

    self.help['qr'] = ['qr [text] - print a scannable qr code from text']
