import common
import out
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
    res = common.run(["pesc", "-q"], msg)
    for line in res.split("\n"):
        await self.message(chan, line)

async def init(self):
    handlers.register(self, modname, pescli)
