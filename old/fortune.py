# REQUIRE exe fortune

import common, out
import handlers

modname = "fortune"

async def fortune(self, chan, src, msg, args, opts):
    """
    :name: fortune
    :hook: cmd
    :help: get a fortune
    :args: @search:str
    :aliases:
    """
    if len(msg) > 0:
        fort = common.run(["fortune", "-sm", msg], "")
    else:
        fort = common.run(["fortune", "-s"], "")
    await out.msg(self, modname, chan, [fort])


async def init(self):
    handlers.register(self, modname, fortune)
