import random

async def owologger(self,c,n,m):
    if m[:len(self.prefix)] == self.prefix:
        return
    if c not in self.owolog:
        self.owolog[c] = []

    self.owolog[c].append([n,m])
    if len(self.owolog[c]) > 333:
        del self.owolog[c][:-300]

async def owoify(self,c,n,m):
    if len(m) < 1:
        m = ["1"]
    try:
        back = int(m[0])+0
    except:
        back = 1
    await self.message(c, await owotext(self, back, c))

async def owotext(self, back, chan):
    if chan in self.owolog and len(self.owolog[chan]) >= back:
        ms = self.owolog[chan][0-back]
        ms[1] = ms[1].replace('r','w').replace('l','w').replace('uck','uwk')
        return '<{}> {} {}'.format(ms[0], ms[1],
            random.choice(['owo', 'uwu', '^w^', 'Owo?', 'OwO', 'oWo', 'UwU']))
    return 'ewwow: my backwog is two showt!'



async def init(self):
    self.owolog = {}
    self.raw['owolog'] = owologger
    self.cmd['owo'] = owoify
    self.help['owo'] = ['owo [num] - owoify the text', 'owo owo uwu']

