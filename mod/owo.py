#
# this module was originally written by xfnw.
# (c) xfnw/lickthecheese <xfnw@tilde.team>
#

import common
import random
import manager
from manager import *

modname = "owo"


@manager.hook(modname, "owo")
@manager.argument("num", argtype=ArgType.INT, optional=True)
@manager.helptext(["owoify the text", "owo owo uwu"])
async def owoify(self, c, n, m):
    ms = ""
    try:
        ms = common.get_backlog_msg(self, c, m)
    except:
        await self.msg(modname, c, [f"my backwog is two showt!"])
        return
    await self.msg(modname, c, [await owotext(self, ms)])


async def owotext(self, msg):
    msg[1] = (
        msg[1]
        .replace("r", "w")
        .replace("l", "w")
        .replace("uck", "uwk")
        .replace("too", "two")
        .replace("ou", "ow")
    )
    owo = random.choice(
        [
            "owo",
            "uwu",
            "^w^",
            "OwO",
            "Owo",
            "owO",
            "Owo?",
            "owO?",
            "UwU",
            "0w0",
            "*w*",
            "+w+",
            "-w-",
        ]
    )
    usr = common.nohighlight(msg[0])
    return f"<{usr}> {msg[1]} {owo}"


async def init(self):
    # self.handle_cmd["owo"] = owoify
    # self.help["owo"] = ["owo [num] - owoify the text", "owo owo uwu"]
    manager.register(self, owoify)
