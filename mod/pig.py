# pig-latin module (·(oo)·) (･ั(00)･ั)
#
# this module is pretty useless, but as it was the first module
# to be added to this bot, I'm leaving it here for, uh, historical
# reasons.

import common
import pig
import handlers
import random
import re

modname = "pig"


async def pigify(self, c, n, m, a, o):
    """
    :name: pig
    :hook: cmd
    :help: convert text to pig-latin
    :args: @text:list
    """
    ms = []
    if len(m) > 0:
        ms = [n, m]
    else:
        try:
            ms = common.get_backlog_msg(self, c, m)
        except:
            await self.msg(modname, c, [f"ymay acklogbay isway ootay ortshay!"])
            return

    pigtext = pig.pigify(ms[1])
    pigface = pig.pig_ascii()

    await self.msg("", c, [f"<{ms[0]}> {pigtext} {pigface}"])


async def init(self):
    handlers.register(self, modname, pigify)
