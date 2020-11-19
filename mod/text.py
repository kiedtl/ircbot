# simple text manipulation stuff

# REQUIRE exe qrencode
# REQUIRE exe figlet
# REQUIRE exe toilet
# REQUIRE exe cowsay
# REQUIRE exe cowthink

import caesar
import config
import common
import handlers
import fmt
import math
import random

modname = "text"

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

async def _cmd_with_args(self, chan, cmd, msg):
    # TODO: throttling, disable in certain channels
    cmd = cmd + msg.split(" ")
    res = common.run(cmd, msg)
    for line in res.split("\n"):
        await self.message(chan, line)


async def qrenco(self, chan, src, msg, args, opts):
    """
    :name: qrenco
    :hook: cmd
    :help: print a scannable qr code from text
    :args: text:str
    :aliases: qr
    """
    # encode text in MicroQR, it's a bit less spammy
    res = common.run(["qrencode", "-Mm2", "-v4",
        "-o-", "-tUTF8", msg], "")
    for line in res.split("\n"):
        await self.message(chan, line)


async def figlet(self, chan, src, msg, args, opts):
    """
    :name: figlet
    :hook: cmd
    :help: make some nice ASCII art with figlet
    :args: text:str
    :aliases:
    """
    await _cmd_with_args(self, chan, ["figlet"], msg)


async def toilet(self, chan, src, msg, args, opts):
    """
    :name: toilet
    :hook: cmd
    :help: make some nice ASCII art with toilet(1)
    :args: text:str
    :aliases: art
    """
    await _cmd_with_args(self, chan, ["toilet", "--irc"], msg)


async def cowsay(self, chan, src, msg, args, opts):
    """
    :name: cowsay
    :hook: cmd
    :help: use cow{say, think}(1) to generate ASCII art
    :args: text:str
    :aliases:
    """
    await _cmd_with_args(self, chan, ["cowsay"], msg)


async def cowthink(self, chan, src, msg, args, opts):
    """
    :name: cowthink
    :hook: cmd
    :help: use cow{say, think}(1) to generate ASCII art
    :args: text:str
    :aliases:
    """
    await _cmd_with_args(self, chan, ["cowthink"], msg)


async def rainbow(self, chan, src, msg, args, opts):
    """
    :name: rainbow
    :hook: cmd
    :help: make rainbows!
    :args: text:str
    :aliases: lolcat
    """
    await self.msg("rainbow", chan, [_irc_rainbow(msg)])

async def communist(self, chan, src, msg, args, opts):
    """
    :name: communist
    :hook: cmd
    :help: seize the means of chaos production, comrade
    :args: text:str
    :aliases: com
    """
    await self.msg("", chan, [_irc_communist(msg)])

async def rot13(self, chan, src, msg, args, opts):
    """
    :name: rot13
    :hook: cmd
    :help: rot13 text
    :args: text:str
    :aliases:
    """
    res = caesar.rot(13)(msg)
    await self.msg("rot", chan, [f"{res}"])


async def rot_n(self, chan, src, msg, _args, opts):
    """
    :name: rot
    :hook: cmd
    :help: like the rot13 command, but rotate message by an arbitrary amount
    :args: rotation:int text:str
    :aliases:
    """
    args = msg.split(" ", 1)

    try:
        rotn = int(args[0])
    except:
        await self.msg("rot", chan, ["invalid rotation amount."])
        return

    res = caesar.rot(rotn)(args[1])
    await self.msg("rot", chan, [f"{res}"])


async def init(self):
    handlers.register(self, modname, qrenco)
    handlers.register(self, modname, figlet)
    handlers.register(self, modname, toilet)
    handlers.register(self, modname, cowsay)
    handlers.register(self, modname, cowthink)
    handlers.register(self, modname, rainbow)
    handlers.register(self, modname, communist)
    handlers.register(self, modname, rot13)
    handlers.register(self, modname, rot_n)
