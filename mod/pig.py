# pig-latin module.
#
# this module is pretty useless, but as it was the first module
# to be added to this bot, I'm leaving it here for, uh, historical
# reasons.

import common
import pig
import random
import re

modname = "pig"


async def pigify(self, c, n, m):
    ms = []
    try:
        ms = common.get_backlog_msg(self, c, m)
    except:
        await self.msg(modname, c, [f"ymay acklogbay isway ootay ortshay!"])
        return

    pigtext = pig.pigify(ms[1])
    pigface = pig.pig_ascii()

    await self.msg(modname, c, [f"<{ms[0]}> {pigtext} {pigface}"])


async def init(self):
    self.handle_cmd["pig"] = pigify
    self.help["pig"] = ["pig [num] - pigify the text (more)", "(·(oo)·) (･ั(00)･ั)"]
