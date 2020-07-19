import dataset
import handlers
import random
import re
import time

MODNAME = 'chat'
LEARNDELAY = 4
ENMUL = 25

qtime = {}
cstate = {}
chatdb = dataset.connect('sqlite:///dat/chat.db')

async def rec(self, m):
    prew = chatdb['prew']
    noch = chatdb['noun']
    beg  = chatdb['beg']
    end  = chatdb['end']
    pre = ''

    words = m.split(' ')
    for w in words:
        if pre == '':
            beg.insert(dict(word=w))
        else:
            prew.insert_ignore(dict(pre=pre, pro=w),['id'])
        pre = w
        noch.insert(dict(word=w))
    end.insert(dict(word=pre))

async def getNoun(self, words, c):
        if c in cstate:
                oldnoun = cstate[c]
        else:
                oldnoun = None

        nouns = [i['word'] for i in chatdb['noun'].find()]
        out = {}
        for i in words:
                out[i] = nouns.count(i)
        noun = min(out, key=out.get)

        conversation = chatdb['conver']
        if oldnoun != None:
                print("adding", [oldnoun,noun])
                conversation.insert_ignore(dict(pre=oldnoun,pro=noun),['id'])

        nextnoun = [i['pro'] for i in conversation.find(pre=noun)]
        print("nextnoun:",nextnoun)
        if len(nextnoun) > 0:
                noun = random.choice(nextnoun)
        cstate[c] = noun
        return noun

async def genOut(self, noun):
    prew = chatdb['prew']
    beg = [ i['word'] for i in chatdb['beg'].find() ]
    end = [ i['word'] for i in chatdb['end'].find() ]
    nouns = [i['word'] for i in chatdb['noun'].find()]
    iter=0
    out = [noun]
    while (out[0] not in beg or nouns.count(out[0])-1 > iter * ENMUL) and iter < 7:
        try:
            out = [ random.choice(list(prew.find(pro=out[0])))['pre'] ] + out
        except IndexError:
            iter += 69
        iter += 1
    iter = 0
    while (out[-1] not in end or nouns.count(out[-1])-1 > iter * ENMUL) and iter < 7:
        try:
            out.append(random.choice(list(prew.find(pre=out[-1])))['pro'])
        except IndexError:
            iter += 69
        iter += 1
    return out


async def learn(self, c, n, m):
    '''
    :name: chat
    :hook: raw
    '''
    if c in qtime and qtime[c] > time.time():
        return

    if m[:len(self.prefix)] == self.prefix:
        return

    if m[:len(self.nickname)] == self.nickname:
        m = m[len(self.nickname):]
        await go(self, c, n, m)
    else:
        if len(re.split('\W', m)) > 1:
            if self.learntime + LEARNDELAY < time.time():
                await rec(self, m)
                self.learntime = time.time()

async def go(self, c, n, m):
        await rec(self, m)
        words = m.split(' ')
        await self.message(c, ' '.join(await genOut(self, await getNoun(self, words, c))))

async def init(self):
    handlers.register(self, MODNAME, learn)

    self.learntime = 0
