import random

async def owoify(self,c,n,m):
    if len(m) < 1:
        m = ['1']
    try:
        back = int(m[0])+0
    except:
        back = 1
    await self.message(c, await owotext(self, back, c))

async def owotext(self, back, chan):
    if chan in self.backlog and len(self.backlog[chan]) >= back:
        ms = self.backlog[chan][0-back]
        ms[1] = ms[1].replace('r','w').replace('l','w').replace('uck','uwk')
        return '<{}> {} {}'.format(ms[0], ms[1],
            random.choice(['owo', 'uwu', '^w^', 'Owo?', 'OwO', 'oWo', 'UwU']))
    return 'ewwow: my backwog is two showt!'

async def init(self):
    self.cmd['owo'] = owoify
    self.help['owo'] = ['owo [num] - owoify the text', 'owo owo uwu']

