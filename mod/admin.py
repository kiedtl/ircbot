#
# this module was originally written by xfnw.
# (c) xfnw/lickthecheese <xfnw@tilde.team>
#

import config
import common, importlib, out, os, time
import traceback
import pprint
import restart as _restart

modname = "admin"


async def dump(self, chan, source, msg):
    """
    dump the contents of self to a file
    for debugging purposes.
    """
    if len(msg) < 1:
        await out.msg(self, modname, chan, ["need filename"])
        return

    with open(msg, "w") as f:
        pprint.pprint(vars(self), stream=f)
        pprint.pprint("\n\n\n", stream=f)
        pprint.pprint(dir(self), stream=f)
    await out.msg(self, modname, chan, ["done"])


async def quit(self, chan, source, msg):
    await self.quit(config.quitmsg)


async def restart(self, chan, source, msg):
    await self.quit(config.quitmsg)
    try:
        _restart.restart()
    except Exception as e:
        self.log(modname, "encountered fatal exception while restarting")
        self.log(modname, f"{repr(e)}")


async def reloadmods(self, chan, source, msg):
    before = time.time()
    await out.msg(self, modname, chan, ["reloading modules..."])

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
        await out.msg(self, modname, chan, [f"segmentation fault", repr(e)])
        self.fndata = fndata
        self.handle_cmd = oldcmd
        self.handle_raw = oldraw
        self.handle_reg = oldreg
        self.aliases = oldali
        self.help = oldhelp
        return

    await out.msg(
        self,
        modname,
        chan,
        [
            "{} modules reloaded in {}s".format(
                len(self.modules), round(time.time() - before, 3)
            )
        ],
    )


async def part(self, chan, source, msg):
    await self.part(msg)


async def join(self, chan, source, msg):
    await self.join(msg)


async def joins(self, chan, source, msg):
    for i in config.prod_chans:
        await self.join(i)


async def aexec(self, code):
    # Make an async function with the code and `exec` it
    exec(f"async def __ex(self): " + "".join(f"\n {l}" for l in code.split("\n")))

    # Get `__ex` from local variables, call it and return the result
    return await locals()["__ex"](self)


async def ev(self, chan, source, msg):
    msg = msg.split(" ")
    try:
        result = await aexec(self, " ".join(msg))
    except Exception as e:
        await out.msg(self, modname, chan, [f"segmentation fault: {repr(e)}"])
        return
    await out.msg(self, modname, chan, [f"result: '{result}'"])


async def send(self, c, n, m):
    msg = m.split(" ")
    await self.message(msg.pop(0), " ".join(msg))


async def shutup(self, c, n, m):
    duration = 5
    if len(m) >= 1:
        try:
            duration = int(m) + 0
        except:
            duration = 5
    self.asleep[c] = time.time() + (duration * 60)
    await out.msg(self, modname, c, [f"disabled for {duration}m"])


async def wake(self, c, n, m):
    self.asleep[c] = time.time()
    await out.msg(self, modname, c, ["I'm back!"])


commands = {
    "coredump": dump,
    "quit": quit,
    "restart": restart,
    "reload": reloadmods,
    "part": part,
    "join": join,
    "eval": ev,
    "send": send,
    "joins": joins,
    "sleep": shutup,
    "wake": wake,
}


async def adminHandle(self, chan, source, msg):
    if await self.is_admin(source):
        msg = msg.split(" ")
        if len(msg) < 1 or not msg[0] in commands:
            await out.msg(self, modname, chan, [self.err_invalid_command])
            return
        print(
            "{} recieved {} signal from {}".format(
                common.modname("admin"), msg[0], source
            )
        )
        await commands[msg.pop(0)](self, chan, source, " ".join(msg))
    else:
        await out.msg(self, modname, chan, ["insufficient privileges"])


async def init(self):
    self.handle_cmd["admin"] = adminHandle
    self.aliases["admin"] = ["a"]

    self.help["admin"] = [
        "admin - various bot owner commands",
        "admin subcommands: coredump quit restart reload part join joins eval send sleep wake",
    ]
    self.help["admin coredump"] = [
        "admin coredump <file> - dump contents of self to file"
    ]
    self.help["admin quit"] = ["admin quit <message> - shutdown bot"]
    self.help["admin restart"] = ["admin restart <message> - restart bot"]
    self.help["admin reload"] = ["admin reload - reload modules and configs"]
    self.help["admin part"] = ["admin part <channel> - make bot leave channel"]
    self.help["admin join"] = ["admin join <channel> -  make bot join channel"]
    self.help["admin joins"] = [
        "admin joins - join channels defined in the admin module"
    ]
    self.help["admin eval"] = ["admin eval <command> - evaluate command"]
    self.help["admin send"] = ["admin send <channel> <message> - send message"]
    self.help["admin sleep"] = [
        "admin sleep [num] - send me into an enchanted sleep for [num] minutes (default: 5m)"
    ]
    self.help["admin wake"] = ["admin wake - wake me up from an enchanted sleep"]
