# On the irc.tilde.chat IRC network, all bots
# are required to respond to "!botlist" and "!rollcall" with
# the bot's owner's nickname and the bot's usage info. This
# module does that, as well as providing the 'ping' and 'whoami'
# commands.

import config as bot_conf
import common
import handlers
import manager
import os
import random

from manager import *

modname = "meta"
BOTLIST = r"^(!rollcall|!botlist)"


@manager.hook(modname, "rollcall", hook=HookType.PATTERN, pattern=BOTLIST)
async def rollcall(self, chan, src, msg):
    await whoami(self, chan, src, msg)


@manager.hook(modname, "ping")
@manager.helptext(["see if I'm responding"])
async def ping(self, chan, src, msg):
    res = random.choice(["you rang?", "yes?", "pong!", "what?", "hmmm?"])
    await self.msg(modname, chan, [f"{src}: {res}"])


@manager.hook(modname, "whoami", aliases=["who"])
@manager.helptext(["list information about this bot"])
async def whoami(self, chan, src, msg):
    source = ""
    if not bot_conf.upstream == None:
        source = "".join([common.nohighlight(i) for i in bot_conf.upstream])

    owner = common.nohighlight(bot_conf.botmaster)
    email = common.nohighlight(bot_conf.email[0]) + "‍＠‍" + bot_conf.email[1]

    response = bot_conf.rollcall_fmt.format(
        nickname=self.nickname,
        description=bot_conf.description,
        prefix=bot_conf.prefix,
        owner=owner,
        source=source,
        email=email,
    )
    await self.msg(modname, chan, [response])


async def init(self):
    manager.register(self, rollcall)
    manager.register(self, ping)
    manager.register(self, whoami)
