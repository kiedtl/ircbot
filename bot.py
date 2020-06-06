#!/usr/bin/env python3

import pydle, asyncio, dataset, sys, os, time
from misc import whoami

class System(pydle.Client):
    async def on_connect(self):
        print('[irc] connected!')

        self.modules = {}
        self.cmd = {}
        self.raw = {}
        self.help = {}

        print('[modules] loading modules...')
        await self.load_mods()
        print('[irc] joining channels')
        for i in self.chansjoin:
            await self.join(i)
        print('[irc] done!')
        print('[irc] attempting to set mode +B')
        await self.set_mode('k', '+B')

    async def load_mods(self):
        for i in [s for s in os.listdir('modules') if '.py' in s]:
            i = i[:-3]
            print('[modules] loading', i)
            m = __import__('modules.' + i)
            m = eval('m.'+i)
            await m.init(self)
            self.modules[i] = m

    async def on_invite(self, channel, by):
        print('[irc] received invite by {} to {}'.format(by, channel))
        await self.join(channel)

    async def on_message(self, chan, source, msg):
        if source != self.nickname:
            for i in self.raw:
                await self.raw[i](self, chan,source,msg)
            if msg == '!botlist' or msg == '!rollcall':
                await whoami(self, chan, source, msg)
                return
            if not chan in self.asleep:
                self.asleep[chan] = time.time()
            if msg[:len(self.prefix)] == self.prefix:
                msg = msg[len(self.prefix):]
                cmd = msg.split(' ')[0]
                msg = msg[len(cmd)+1:]
                if cmd in self.cmd:
                    if self.asleep[chan] < time.time() or cmd == 'admin':
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

    async def on_user_mode_change(self, modes):
        print('[irc] mode changed: {}'.format(modes))

if __name__ == '__main__':
    client = System('k', realname='spacehare\'s bot')
    client.prefix = ':'
    client.asleep = {}
    client.run('localhost', tls=False, tls_verify=False)
