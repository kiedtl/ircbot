# if someone says /2/2, respond :)

import configuration
import manager
import random
import re

from manager import *

RESPONSE = [
    "fuck",
    "stahp",
    "no u",
    "you're clogging my logs",
    "opers: halp",
    "stop spamming",
    "irssi--",
]
PERCENTAGE = 80

modname = "bufcmdfsck"
IS_BUFCMD = r"^(\/([0-9])+)+$"


@manager.hook(modname, "bufcmdfilter", hook=HookType.PATTERN, pattern=IS_BUFCMD)
@manager.config("respond-to-bufcmd", ConfigScope.CHAN, desc="True or False", cast=bool)
async def bufcmd_filter(self, chan, src, msg):
    if src == self.nickname:
        return

    enabled = configuration.get(self.network, chan, "respond-to-bufcmd", cast=bool)
    if not enabled:
        return

    if random.uniform(0, 100) < PERCENTAGE:
        await self.message(chan, random.choice(RESPONSE))


async def init(self):
    manager.register(self, bufcmd_filter)
