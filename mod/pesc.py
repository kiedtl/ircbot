import common
import out
import handlers

modname = "pesc"

# NOTE: this is *very* WIP
async def pescli(self, chan, src, msg, args, opts):
    """
    :name: pescli
    :hook: cmd
    :help: execute Pesc statements (see pesc(7))
    :args: @command:str
    :aliases: calc pesc
    """
    res = common.run(["/home/kiedtl/local/bin/pescli", "-q"], msg)
    await out.msg(self, modname, chan, [res[0]])

async def init(self):
    handlers.register(self, modname, pescli)
