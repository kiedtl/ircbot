# TODO: move to help module, admin module
# TODO: rename "meta" module

import config
import common
import handlers
import os
import random

modname = "misc"

async def list_mods(self, chan, src, msg, args, opts):
    """
    :name: modules
    :hook: cmd
    :help: list loaded modules
    :args:
    :aliases:
    """
    mods = ", ".join(sorted(list(self.modules.keys())))
    await self.msg(modname, chan, [f"loaded: {mods}"])


async def load_mod(self, chan, src, msg, args, opts):
    """
    :name: loadmodule
    :hook: cmd
    :help: load an unloaded module from $ROOT/mod/
    :args: module:str
    :require_admin:
    :aliases: load
    """
    mod = msg.split()[0]
    mods = [s for s in os.listdir("mod") if ".py" in s]
    if not f"{mod}.py" in mods:
        await self.msg("modules", chan, ["no such module"])
        return

    self.log("modules", f"loading {mod}")
    m = __import__("mod." + mod)
    m = eval("m." + mod)
    await m.init(self)
    self.modules[mod] = m
    await self.msg(modname, chan, ["loaded module"])


async def unload_mod(self, chan, src, msg, args, opts):
    """
    :name: unloadmodule
    :hook: cmd
    :help: unload an loaded module
    :args: module:str
    :require_admin:
    :aliases: unload
    """
    mod = msg.split()[0]
    if not mod in self.modules:
        await self.msg(modname, chan, ["no such module"])
        return
    else:
        del self.modules[mod]
        await self.msg(modname, chan, ["unloaded module"])


async def ping(self, chan, src, msg, args, opts):
    """
    :name: ping
    :hook: cmd
    :help: see if I'm responding
    :args:
    :aliases:
    """
    res = random.choice(
        ["you rang?", "yes?", "pong!", "what?", "hmmm?", "at your service!"]
    )
    await self.msg(modname, chan, [f"{src}: {res}"])


async def whoami(self, chan, src, msg, args, opts):
    """
    :name: whoami
    :hook: cmd
    :help: list information about this bot
    :args:
    :aliases: who
    """
    source = ""
    if not config.upstream == None:
        source = "".join([common.nohighlight(i) for i in config.upstream])

    owner = common.nohighlight(config.botmaster)
    email = common.nohighlight(config.email[0]) + "‍＠‍" + config.email[1]

    response = config.rollcall_fmt.format(
            nickname=self.nickname,
            description=config.description,
            prefix=config.prefix,
            owner=owner, source=source, email=email
    )
    await self.msg(modname, chan, [response])


async def init(self):
    handlers.register(self, modname, list_mods)
    handlers.register(self, modname, load_mod)
    handlers.register(self, modname, unload_mod)
    handlers.register(self, modname, whoami)
    handlers.register(self, modname, ping)
