import random
import re

def twoch(s):
    if len(s) < 2:
        return s[0]
    else:
        return s[0] + s[1]

def hasupper(s):
    has = False
    for ch in s:
        if (ch.isupper()):
            has = True
    return has

async def piglogger(self, c, n, m):
    print('[LOGGER] logged message')
    if m[:len(self.prefix)] == self.prefix:
        return
    if c not in self.piglog:
        self.piglog[c] = []

    self.piglog[c].append([n,m])
    if len(self.piglog[c]) > 512:
        del self.piglog[c][:-256]

async def pigify(self, c, n, m):
    if len(m) < 1:
        m = ["1"]
    try:
        back = int(m[0])+0
    except:
        back = 1
    await self.message(c, await pigtext(self, back, c))

async def pigtext(self, back, chan):
    if chan in self.piglog and len(self.piglog[chan]) >= back:
        ms = self.piglog[chan][0-back]
        data = re.split(r'([!-/:-@\[-`{-~\ ]+)', ms[1])

        list = ['sh', 'gl', 'ch', 'ph', 'tr', 'br', 'fr',
                'bl', 'gr', 'st', 'sl', 'cl', 'pl', 'fl']

        for k in range(len(data)):
            i = data[k]
            if len(i) == 0:
                continue
            if i[0] in ['a', 'e', 'i', 'o', 'u']:
                data[k] = i + 'ay'
            elif twoch(i) in list:
                data[k] = i[2:] + i[:2] + 'ay'
            elif i.isalpha() == False:
                data[k] = i
            else:
                data[k] = i[1:] + i[0] + 'ay'

            if (hasupper(data[k])):
                data[k] = data[k].lower()
                data[k] = data[k][:1].upper() + data[k][1:]

        return '<{}> {} {}'.format(ms[0], ''.join(data),
                random.choice(['(･ั(00)･ั)', '(´·(oo)·`)', '(·(oo)·)', '(v -(··)-v)', '(> (··) <)', '(° (··) °)']))
    return 'errorway: ymay acklogbay isway ootay ortshay!'

async def init(self):
    self.piglog = {}
    self.raw['piglog'] = piglogger
    self.cmd['pig'] = pigify
    self.help['pig'] = ['pig [num] - pigify the text (more)',
            '(·(oo)·) (･ั(00)･ั)']
