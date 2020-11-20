import common
import handlers

modname = "status"


async def status(self, chan, src, msg):
    """
    :name: sysinfo
    :hook: cmd
    :help: sysinfo - retrieve info for the tilde.team server
    :args:
    :aliases:
    """
    res = common.run(["bin/sysinfo"], "")
    await self.msg(modname, chan, [f"~team status: {res}"])


async def init(self):
    handlers.register(self, modname, status)
