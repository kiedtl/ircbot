# simple text manipulation stuff

import caesar
import config
import common
import handlers
import fmt
import manager
import math
import pig
import random
import re
import utils

from manager import *
from handlers import *

modname = "text"


def _owo_text(text):
    #
    # this module was originally written by xfnw.
    # (c) xfnw/lickthecheese <xfnw@tilde.team>
    #

    text = (
        text.replace("r", "w")
        .replace("l", "w")
        .replace("uck", "uwk")
        .replace("too", "two")
        .replace("ou", "ow")
    )

    owo = random.choice(
        ["owo", "uwu", "^w^", "OwO", "Owo", "owO", "Owo?", "owO?", "UwU", "0w0"]
    )

    return f"{text} {owo}"


def _irc_rainbow(text):
    buf = ""
    rainbow = [fmt.blue, fmt.cyan, fmt.yellow, fmt.red, fmt.magenta]
    ctr = random.uniform(0, len(rainbow))
    for char in text:
        buf += rainbow[math.floor(ctr) % len(rainbow)](char)
        ctr += 0.5
    return buf


def _irc_communist(text):
    return f"\x038,5\x02 ☭ {text.upper()} ☭ \x0f"


def _mock_text(text):
    cases = utils.enum(UPPER=0, LOWER=1)
    dest = ""
    case = cases.LOWER
    for char in text:
        if char.isalpha():
            if case == cases.LOWER:
                char = char.lower()
                case = cases.UPPER
            elif case == cases.UPPER:
                char = char.upper()
                case = cases.LOWER
        dest += char
    return dest


@manager.hook(modname, "pig", desc="convert text to pig latin")
@manager.arguments([Arg("text", optional=True)])
async def pigify(self, c, n, m):
    # pig-latin module (·(oo)·) (･ั(00)･ั)
    #
    # this command is pretty useless, but as it was the first module
    # to be added to this bot, I'm leaving it here for, uh, historical
    # reasons.

    ms = []
    if len(m) > 0:
        ms = [n, m]
    else:
        try:
            ms = common.get_backlog_msg(self, c, m)
        except:
            await self.msg(modname, c, [f"ymay acklogbay isway ootay ortshay!"])
            return

    pigtext = pig.pigify(ms[1])
    pigface = pig.pig_ascii()
    usr = fmt.zwnj(ms[0])

    return (Msg.RAW, f"<{usr}> {pigtext} {pigface}")


@manager.hook(modname, "owo", desc="owoify the text")
@manager.arguments([Arg("num", argtype=ArgType.INT, optional=True)])
async def owoify(self, chan, src, msg):
    ms = ""
    try:
        ms = common.get_backlog_msg(self, chan, msg)
    except:
        await self.msg(modname, chan, [f"my backwog is two showt!"])
        return
    usr = fmt.zwnj(ms[0])
    res = _owo_text(ms[1])
    return (Msg.RAW, f"<{usr}> {res}")


@manager.hook(modname, "mock")
@manager.arguments([Arg("user")])
@manager.helptext(["mock user's last message by printing it in aLtErNaTiNg cApS"])
async def mock(self, chan, src, msg):
    ms = None
    if chan in self.backlog:
        backlog = list(reversed(self.backlog[chan]))
        for back_msg in backlog:
            if back_msg[0] == msg:
                ms = back_msg
                break

    if not ms:
        await self.msg(modname, chan, [f"couldn't find anything to mock"])
        return

    mocked = _mock_text(ms[1])
    usr = fmt.zwnj(ms[0])
    return (Msg.RAW, f"<{usr}> {mocked}")


async def rainbow(self, chan, src, msg):
    """
    :name: rainbow
    :hook: cmd
    :help: make rainbows!
    :args: text:str
    :aliases: lolcat
    """
    return (Msg.RAW, _irc_rainbow(msg))


async def communist(self, chan, src, msg):
    """
    :name: communist
    :hook: cmd
    :help: seize the means of chaos production, comrade
    :args: text:str
    :aliases: com comm
    """
    return (Msg.RAW, _irc_communist(msg))


async def rot13(self, chan, src, msg):
    """
    :name: rot13
    :hook: cmd
    :help: rot13 text
    :args: text:str
    """
    return (Msg.OK, caesar.rot(13)(msg))


async def rot_n(self, chan, src, msg):
    """
    :name: rot
    :hook: cmd
    :help: like the rot13 command, but rotate message by an arbitrary amount
    :args: rotation:int text:str
    """
    args = msg.split(" ", 1)

    try:
        rotn = int(args[0])
    except:
        return (Msg.ERR, "invalid rotation amount.")

    res = caesar.rot(rotn)(args[1])
    return (Msg.OK, caesar.rot(rotn)(args[1]))


async def init(self):
    manager.register(self, owoify)
    manager.register(self, pigify)
    manager.register(self, mock)

    handlers.register(self, modname, rainbow)
    handlers.register(self, modname, communist)
    handlers.register(self, modname, rot13)
    handlers.register(self, modname, rot_n)
