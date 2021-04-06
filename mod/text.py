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


def _irc_capitalist(text):
    #return f"\x037,3\x02 $$$ {text.upper()} $$$ \x0f"
    return f"\x038,3\x02 $$$ {text.upper()} $$$ \x0f"


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


@manager.hook(modname, "rainbow", aliases=["lolcat"])
@manager.arguments([Arg("text")])
@manager.helptext([_irc_rainbow("make rainbows~~")])
async def rainbow(self, chan, src, msg):
    return (Msg.RAW, _irc_rainbow(msg))


@manager.hook(modname, "communist", aliases=["com"])
@manager.arguments([Arg("text")])
@manager.helptext([_irc_communist("seize the means of production, comrade")])
async def communist(self, chan, src, msg):
    return (Msg.RAW, _irc_communist(msg))


@manager.hook(modname, "capitalist", desc="$.$", aliases=["cap"])
@manager.arguments([Arg("text")])
async def capitalist(self, chan, src, msg):
    return (Msg.RAW, _irc_capitalist(msg))


@manager.hook(modname, "rot13", desc="rot13 text")
@manager.arguments([Arg("text")])
async def rot13(self, chan, src, msg):
    return (Msg.OK, caesar.rot(13)(msg))


@manager.hook(modname, "rot", desc="like rot13, but rotate message by an arbitrary amount")
@manager.arguments([Arg("rotation", argtype=ArgType.INT), Arg("text")])
async def rot_n(self, chan, src, msg):
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
    manager.register(self, capitalist)
    manager.register(self, rainbow)
    manager.register(self, communist)
    manager.register(self, rot13)
    manager.register(self, rot_n)
