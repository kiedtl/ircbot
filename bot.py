#!/usr/bin/env python3

import pydle, asyncio, dataset, sys, os, time

class System(pydle.Client):
    async def on_connect(self):
        print('[IRC] connected!')

        self.modules = {}
        self.cmd = {}
        self.raw = {}
        self.help = {}

        print('[MODULES] loading modules...')
        await self.loadMods()
        print('[IRC] joining channels')
        for i in self.chansjoin:
            await self.join(i)
        print('[IRC] done!')

    async def loadMods(self):
        for i in [s for s in os.listdir('modules') if ".py" in s]:
            i = i[:-3]
            print('[MODULES] loading', i)
            m = __import__("modules."+i)
            m = eval('m.'+i)
            await m.init(self)
            self.modules[i] = m

    async def on_invite(self, channel, by):
        print('{} invited me to {}!'.format(by, channel))
        await self.join(channel)

    async def on_message(self, chan, source, msg):
        if source != self.nickname:
            for i in self.raw:
                await self.raw[i](self, chan,source,msg)
            if msg == '!botlist':
                await self.message(chan, 'Hi! I\'m spacehare\'s bot.')
            if msg[:len(self.prefix)] == self.prefix:
                msg = msg[len(self.prefix):]
                cmd = msg.split(' ')[0]
                msg = msg[len(cmd)+1:]
                if cmd in self.cmd:
                    await self.cmd[cmd](self, chan, source, msg)


    async def is_admin(self, nickname):
        admin = False

        # check the WHOIS info to see if the source has identified.
        # this is a blocking operation, so use yield.
        if nickname in self.admins:
            info = await self.whois(nickname)
            admin = info['identified']
        return admin

    async def on_private_message(self, trash, source, msg):
        if source != self.nickname:
            for i in self.raw:
                await self.raw[i](self, chan,source,msg)
            if msg[:len(self.prefix)] == self.prefix:
                msg = msg[len(self.prefix):]
                cmd = msg.split(' ')[0]
                msg = msg[len(cmd)+1:]
                if cmd in self.cmd:
                    await self.cmd[cmd](self, chan, source, msg)

if __name__ == "__main__":
    client = System('k', realname='spacehare\'s annoying bot')
    client.admins = ['kiedtl', 'spacehare', 'ben', 'cmccabe',
            'gbmor', 'tomasino', 'ubergeek', 'deepend',
            'calamitous','khuxkm']
    client.prefix = ':'
    client.run('localhost', tls=False, tls_verify=False)
