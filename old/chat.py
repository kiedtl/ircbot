import dataset
import humanize
import os
#import handlers
import random
import re
import time

WSPLIT = re.compile(r'[!-/:-@\[-`{-~\ 0-9]+')
MODNAME = 'chat'
LEARNDELAY = 4
ENMUL = 25

qtime = {}
cstate = {}
chatdb = dataset.connect('sqlite:///dat/chat.db')

class Tmp():
    pass

#async def rec(self, m):
def rec(self, m):
    prew = chatdb['prew']
    noch = chatdb['noun']
    beg  = chatdb['beg']
    end  = chatdb['end']
    pre = ''

    words = WSPLIT.split(m)
    for w in words:
        if pre == '':
            beg.insert(dict(word=w))
        else:
            prew.insert_ignore(dict(pre=pre, pro=w),['id'])
        pre = w
        noch.insert(dict(word=w))
    end.insert(dict(word=pre))

#async def getNoun(self, words, c):
def getNoun(self, words, c):
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

#async def genOut(self, noun):
def genOut(self, noun):
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


#async def learn(self, c, n, m):
def learn(self, c, n, m):
    '''
    :name: chat
    :hook: raw
    '''
    #if c in qtime and qtime[c] > time.time():
    #    return

    #if m[:len(self.prefix)] == self.prefix:
    #    return

    if m[:len(self.nickname)] == self.nickname:
        m = m[len(self.nickname):]
        #await go(self, c, n, m)
        go(self, c, n, m)
    else:
        if len(WSPLIT.split(m)) > 1:
            #if self.learntime + LEARNDELAY < time.time():
                #await rec(self, m)
            rec(self, m)
            self.learntime = time.time()

#async def go(self, c, n, m):
def go(self, c, n, m):
    #    await rec(self, m)
    #    words = WSPLIT.split(m)
    #    await self.message(c, ' '.join(await genOut(self, await getNoun(self, words, c))))
    pass

#async def init(self):
    #handlers.register(self, MODNAME, learn)

self = Tmp()
self.learntime = 0
self.nickname = 'tmp'

with open('/home/kiedtl/doc/lotr-fixed.txt') as logf:
    stuff = logf.read().split('\n')
    ln = len(stuff)
    chatdb.begin()
    for i in range(0, ln):
        if i % 64 == 0:
            print(f'\rlearning... [{i}/{ln}]', end='')
        learn(self, '', '', stuff[i])
    print(f'\nwriting...', end='')
    chatdb.commit()
    print(f' done')
