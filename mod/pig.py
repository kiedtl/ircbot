import common
import out, random, re

modname = 'pig'
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
        ms = common.get_backlog_msg(self, c, m)
    except:
        await out.msg(self, modname, c, [f'ymay acklogbay isway ootay ortshay!'])
        return
    await out.msg(self, modname, c, [await pigtext(self, ms)])

async def pigtext(self, ms):
    # filter out ZWNJ's
    ms[1] = ms[1].replace('\u200c', '')
    data = re.split(r'([!-/:-@\[-`{-~\ 0-9]+)', ms[1])

    disyms = ['sh', 'gl', 'ch', 'ph', 'tr', 'br', 'fr',
        'bl', 'gr', 'st', 'sl', 'cl', 'pl', 'fl']

    for k in range(len(data)):
        i = data[k]
        if len(i) == 0:
            continue

        # translation
        if i[0] in vowels:
            data[k] = i + 'way'
        elif twoch(i) in disyms:
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
    usr = common.nohighlight(ms[0])
    return f'<{usr}> {"".join(data)} {pig}'

async def init(self):
    self.handle_cmd['pig'] = pigify
    self.help['pig'] = ['pig [num] - pigify the text (more)',
            '(·(oo)·) (･ั(00)･ั)']
