import handlers
import out

modname = "more"


async def more(self, ch, src, msg, args, opts):
    """
    :name: more
    :hook: cmd
    :help: view more text
    :args:
    :aliases: m
    """

    await out.more(self, ch)


async def init(self):
    handlers.register(self, modname, more)
