from common import get_backlog_msg
import random, re

vowels = ['a', 'e', 'i', 'o', 'u']

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

async def pigify(self, c, n, m):
    ms = []
    try:
        ms = get_backlog_msg(self, c, m)
    except:
        await self.message(c, 'errorway: ymay acklogbay isway ootay ortshay!')
        return
    await self.message(c, await pigtext(self, ms))

async def pigtext(self, ms):
    data = re.split(r'([!-/:-@\[-`{-~\ ]+)', ms[1])

    list = ['sh', 'gl', 'ch', 'ph', 'tr', 'br', 'fr',
        'bl', 'gr', 'st', 'sl', 'cl', 'pl', 'fl']

    for k in range(len(data)):
        i = data[k]
        if len(i) == 0:
            continue

        # translation
        if i[0] in vowels:
            data[k] = i + 'way'
        elif twoch(i) in list:
            data[k] = i[2:] + i[:2] + 'ay'
        elif i.isalpha() == False:
            data[k] = i
        else:
            data[k] = i[1:] + i[0] + 'ay'

        # correct captalization
        # e.g. "You've" => "ouYay'evay" => "Ouyay'evay"
        if (hasupper(data[k])):
            data[k] = data[k].lower()
            data[k] = data[k][:1].upper() + data[k][1:]

    pig = random.choice(['(･ั(00)･ั)', '(´·(oo)·`)', '(·(oo)·)',
        '(v -(··)-v)', '(> (··) <)', '(° (··) °)'])
    return '<{}> {} {}'.format(ms[0], ''.join(data), pig)

async def init(self):
    self.cmd['pig'] = pigify
    self.help['pig'] = ['pig [num] - pigify the text (more)',
            '(·(oo)·) (･ั(00)･ั)']
