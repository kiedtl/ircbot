from common import get_backlog_msg
import random

async def owoify(self, c, n, m):
    ms = ''
    try:
        ms = get_backlog_msg(self, c, m)
    except:
        await self.message(c, 'ewwow: my backwog is two showt!')
        return
    await self.message(c, await owotext(self, ms))

async def owotext(self, msg):
    msg[1] = msg[1].replace('r','w').replace('l','w').replace('uck','uwk').replace('too', 'two')
    owo = random.choice(['owo', 'uwu', '^w^', 'OwO', 'Owo',
        'owO', 'Owo?', 'owO?', 'UwU', '0w0', '*w*', '+w+', '-w-'])
    return '<{}> {} {}'.format(msg[0], msg[1], owo)

async def init(self):
    self.cmd['owo'] = owoify
    self.help['owo'] = ['owo [num] - owoify the text', 'owo owo uwu']
