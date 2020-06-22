#!/usr/bin/env python3

import asyncio
import config
import os
import pydle
import sys
import time

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

        if config.set_botmode:
            print('[irc] attempting to set mode +B')
            await self.set_mode(self.nickname, '+B')

    async def load_mods(self):
        for i in [s for s in os.listdir('modules') if '.py' in s]:
            i = i[:-3]
            print('[modules] loading', i)
            m = __import__('modules.' + i)
            m = eval('m.' + i)
            await m.init(self)
            self.modules[i] = m

    async def on_invite(self, chan, by):
        print('[irc] received invite by {} to {}'.format(by, chan))

        if config.join_on_invite:
            if chan not in config.bannedchans:
                await self.join(chan)

    async def on_message(self, chan, source, msg):
        for i in self.raw:
            await self.raw[i](self, chan,source,msg)
        if source != self.nickname:
            if msg == '!botlist' or msg == '!rollcall':
                if config.respond_to_rollcall:
                    await whoami(self, chan, source, msg)
                return
            if not chan in self.asleep:
                self.asleep[chan] = time.time()
            if msg[:len(self.prefix)] == self.prefix:
                msg = msg[len(self.prefix):]
                cmd = msg.split(' ')[0]
                msg = msg[len(cmd) + 1:]
                if cmd in self.cmd:
                    if self.asleep[chan] < time.time() or cmd == 'admin':
                        await self.cmd[cmd](self, chan, source, msg)
                    print('[cmd] recieved command {} from {} in {}'
                        .format(cmd, source, chan))

    async def is_admin(self, nickname):
        admin = False

        # check the WHOIS info to see if the source has identified.
        # this is a blocking operation, so use yield.
        if nickname in config.admins:
            info = await self.whois(nickname)
            admin = info['identified']
        return admin

    async def on_private_message(self, chan, source, msg):
        await self.on_message(chan, source, msg)

    async def on_user_mode_change(self, modes):
        print('[irc] mode changed: {}'.format(modes))

if __name__ == '__main__':
    client = System(config.nickname, realname=config.realname)
    client.prefix = config.prefix
    client.asleep = {}
    client.run(config.server, tls=config.tls, tls_verify=config.tls_verify)
