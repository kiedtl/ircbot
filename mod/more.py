import handlers

modname = "more"


async def more(self, ch, src, msg):
    """
    :name: more
    :hook: cmd
    :help: view more text
    :args:
    :aliases: m
    """

    await self.more(ch)


async def init(self):
    handlers.register(self, modname, more)
