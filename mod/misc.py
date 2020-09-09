# REQUIRE file bin/sysinfo

import config
import common
import handlers
import out
import os
import random


async def list_mods(self, chan, src, msg):
    mods = ", ".join(sorted(list(self.modules.keys())))
    await out.msg(self, "modules", chan, [f"loaded: {mods}"])


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
    mods = [s for s in os.listdir('mod') if '.py' in s]
    if not f'{mod}.py' in mods:
        await out.msg(self, 'modules', chan, ['no such module'])
        return

    self.log('modules', f'loading {mod}')
    m = __import__('mod.' + mod)
    m = eval('m.' + mod)
    await m.init(self)
    self.modules[mod] = m
    await out.msg(self, 'modules', chan, ['loaded module'])

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
        await out.msg(self, 'modules', chan, ['no such module'])
        return
    else:
        del self.modules[mod]
        await out.msg(self, 'modules', chan, ['unloaded module'])


async def ping(self, chan, src, msg):
    res = random.choice(
        ["you rang?", "yes?", "pong!", "what?", "hmmm?", "at your service!"]
    )
    await out.msg(self, "ping", chan, [f"{src}: {res}"])


async def whoami(self, chan, src, msg):
    owner = common.nohighlight(config.botmaster)
    email = common.nohighlight(config.email[0]) + "‍＠‍" + config.email[1]
    source = "".join([common.nohighlight(i) for i in config.upstream])
    await out.msg(self, "who", chan, [f"I'm {self.nickname}, {owner}'s bot."])
    await out.msg(self, "who", chan, [f"upstream: {source}"])
    await out.msg(self, "who", chan, [f"reporting issues: {email}"])
    await out.msg(self, "who", chan, [f"for usage info, try {config.prefix}help"])


async def init(self):
    self.handle_cmd["modules"] = list_mods
    self.handle_cmd["ping"] = ping
    self.handle_cmd["who"] = whoami

    self.help["modules"] = ["modules - list loaded modules"]
    self.help["ping"] = ["ping - check if I'm responding"]
    self.help["who"] = ["who - get information about my owner"]

    handlers.register(self, 'modules', load_mod)
    handlers.register(self, 'modules', unload_mod)
