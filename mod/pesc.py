import common
import handlers

modname = "pesc"

# NOTE: this is *very* WIP
async def pescli(self, chan, src, msg):
    """
    :name: pescli
    :hook: cmd
    :help: execute Pesc statements (see pesc(7))
    :args: @command:str
    :aliases: calc pesc
    """
    res = common.run(["/home/kiedtl/local/bin/pescli", "-q"], msg)
    for line in res.split("\n"):
        await self.msg(modname, chan, [line])
        break


async def init(self):
    handlers.register(self, modname, pescli)
