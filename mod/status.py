import common
import handlers
import out

modname = "status"


async def status(self, chan, src, msg, args, opts):
    """
    :name: sysinfo
    :hook: cmd
    :help: sysinfo - retrieve info for the tilde.team server
    :args:
    :aliases:
    """
    res = common.run(["bin/sysinfo"], "")
    await out.msg(self, modname, chan, [f"~team status: {res}"])


async def init(self):
    handlers.register(self, modname, status)