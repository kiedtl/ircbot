import common
import handlers
import out

modname = "dunnet"


async def dunnet_run(self, chan, src, msg, args, opts):
    """
    :name: dunnet
    :hook: cmd
    :help: play dunnet, a text adventure game from emacs!
    :args: command:str
    :aliases: dun
    :require_identified:
    """
    res = common.run(["bin/dunnet", src, msg], "")
    for line in res.split('\n'):
        await out.msg(self, modname, chan, [f"{line}"])


async def init(self):
    handlers.register(self, modname, dunnet_run)
