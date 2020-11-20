#
# this module was originally written by xfnw.
# (c) xfnw/lickthecheese <xfnw@tilde.team>
#

import config
import common, importlib, os, time
import traceback
import handlers
import pprint
import restart as _restart

modname = "admin"


async def _aexec(self, code):
    # Make an async function with the code and `exec` it
    exec(f"async def __ex(self): " + "".join(f"\n {l}" for l in code.split("\n")))

    # Get `__ex` from local variables, call it and return the result
    return await locals()["__ex"](self)


async def dump(self, chan, source, msg, args, opts):
    """
    :name: coredump
    :hook: cmd
    :help: dump the bot's global variables to a file for debugging purposes.
    :args: file:str
    :require_admin:
    :aliases:
    """
    with open(msg, "w") as f:
        pprint.pprint(vars(self), stream=f)
        pprint.pprint("\n\n\n", stream=f)
        pprint.pprint(dir(self), stream=f)
    await self.msg(modname, chan, ["done"])


async def quit(self, chan, source, msg, args, opts):
    """
    :name: quit
    :hook: cmd
    :help: shutdown the bot
    :args: @msg:str
    :require_admin:
    :aliases:
    """
    quitmsg = config.quitmsg
    if len(msg) > 1:
        quitmsg = msg
    await self.quit(quitmsg)


async def restart(self, chan, source, msg, args, opts):
    """
    :name: restart
    :hook: cmd
    :help: restart the bot
    :args:
    :require_admin:
    :aliases:
    """
    await self.quit(config.quitmsg)
    try:
        _restart.restart()
    except Exception as e:
        self.log(modname, "encountered fatal exception while restarting")
        self.log(modname, f"{repr(e)}")
        exit(1)


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


async def reloadmods(self, chan, source, msg, args, opts):
    """
    :name: reload
    :hook: cmd
    :help: reload the bot's modules
    :args:
    :require_admin:
    :aliases: rl
    """
    before = time.time()
    await self.msg(modname, chan, ["reloading modules..."])

    fndata = self.fndata
    oldcmd = self.handle_cmd
    oldraw = self.handle_raw
    oldreg = self.handle_reg
    oldali = self.aliases
    oldhelp = self.help

    self.fndata = {}
    self.handle_cmd = {}
    self.handle_raw = {}
    self.handle_reg = {}
    self.aliases = {}
    self.help = {}

    try:
        for i in self.modules:
            importlib.reload(self.modules[i])
            await self.modules[i].init(self)
    except Exception as e:
        traceback.print_tb(e.__traceback__)
        await self.msg(modname, chan, [f"segmentation fault", repr(e)])
        self.fndata = fndata
        self.handle_cmd = oldcmd
        self.handle_raw = oldraw
        self.handle_reg = oldreg
        self.aliases = oldali
        self.help = oldhelp
        return

    await self.msg(
        modname,
        chan,
        [
            "{} modules reloaded in {}s".format(
                len(self.modules), round(time.time() - before, 3)
            )
        ],
    )


async def part(self, chan, source, msg, args, opts):
    """
    :name: part
    :hook: cmd
    :help: make bot leave a channel
    :args: channel:str
    :require_admin:
    :aliases:
    """
    await self.part(msg)


async def join(self, chan, source, msg, args, opts):
    """
    :name: join
    :hook: cmd
    :help: make bot join a channel
    :args: channel:str
    :require_admin:
    :aliases:
    """
    await self.join(msg)


async def joinall(self, chan, source, msg, args, opts):
    """
    :name: joinall
    :hook: cmd
    :help: make bot join all channels listed in the bot's config
    :args:
    :require_admin:
    :aliases: joins
    """
    for i in config.prod_chans:
        await self.join(i)


async def ev(self, chan, source, msg, args, opts):
    """
    :name: eval
    :hook: cmd
    :help: evaluate some Python code
    :args: code:list
    :require_admin:
    :aliases: ev
    """
    msg = msg.split(" ")
    try:
        result = await _aexec(self, " ".join(msg))
    except Exception as e:
        await self.msg(modname, chan, [f"segmentation fault: {repr(e)}"])
        return
    await self.msg(modname, chan, [f"result: '{result}'"])


async def send(self, c, n, m, args, opts):
    """
    :name: send
    :hook: cmd
    :help: send <text> to <channel>
    :args: channel:str text:list
    :require_admin:
    :aliases:
    """
    msg = m.split(" ")
    await self.message(msg.pop(0), " ".join(msg))


async def shutup(self, c, n, m, args, opts):
    """
    :name: sleep
    :hook: cmd
    :help: disable the bot in the current channel for [minutes] (default is 5)
    :args: @minutes:int
    :require_admin:
    :aliases:
    """
    duration = 5
    if len(m) >= 1:
        try:
            duration = int(m) + 0
        except:
            pass
    self.asleep[c] = time.time() + (duration * 60)
    await self.msg(modname, c, [f"disabled for {duration}m"])


async def wake(self, c, n, m, args, opts):
    """
    :name: wake
    :hook: cmd
    :help: enable the bot in the current channel
    :args:
    :require_admin:
    :aliases:
    """
    self.asleep[c] = time.time()
    await self.msg(modname, c, ["I'm back!"])


async def init(self):
    handlers.register(self, modname, dump)
    handlers.register(self, modname, quit)
    handlers.register(self, modname, restart)
    handlers.register(self, modname, load_mod)
    handlers.register(self, modname, unload_mod)
    handlers.register(self, modname, reloadmods)
    handlers.register(self, modname, part)
    handlers.register(self, modname, join)
    handlers.register(self, modname, joinall)
    handlers.register(self, modname, ev)
    handlers.register(self, modname, send)
    handlers.register(self, modname, shutup)
    handlers.register(self, modname, wake)
