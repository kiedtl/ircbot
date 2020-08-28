#
# this module was originally written by xfnw.
# (c) xfnw/lickthecheese <xfnw@tilde.team>
#

import common
import out, random

modname = "owo"


async def owoify(self, c, n, m):
    ms = ""
    try:
        ms = common.get_backlog_msg(self, c, m)
    except:
        await out.msg(self, modname, c, [f"my backwog is two showt!"])
        return
    await out.msg(self, modname, c, [await owotext(self, ms)])


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
    self.handle_cmd["owo"] = owoify
    self.help["owo"] = ["owo [num] - owoify the text", "owo owo uwu"]
