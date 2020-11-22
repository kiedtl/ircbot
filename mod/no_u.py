# if someone says no u, respond

import configuration
import manager
import time
from manager import *

modname = "nou"
YES_U = f"^no [uùúüû]$"

TIMEOUT = 2.2
timeouts = {}

@manager.hook(modname, "noufilter", hook=HookType.PATTERN, pattern=YES_U)
@manager.config("respond-to-nou", ConfigScope.CHAN, desc="True or False", cast=bool)
@manager.config("respond-to-nou", ConfigScope.USER, desc="True or False", cast=bool)
async def filternou(self, chan, src, msg):
    if src == self.nickname:
        return

    if not self.users[src]['identified']:
        return
    user = self.users[src]['account']

    enabled_chan = configuration.get(self.network, chan, "respond-to-nou", cast=bool)
    enabled_user = configuration.get(self.network, user, "respond-to-nou", cast=bool)

    if not enabled_chan or not enabled_user:
        return

    # don't say "no u" twice within the same TIMEOUT-second period
    if chan in timeouts and timeouts[chan] + TIMEOUT >= time.time():
        return
    timeouts[chan] = time.time()

    await self.message(chan, "no u")

async def init(self):
    manager.register(self, filternou)
