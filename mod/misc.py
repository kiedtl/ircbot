# REQUIRE file bin/sysinfo

import config
import common
import out
import random


async def list_mods(self, chan, src, msg):
    mods = ", ".join(sorted(list(self.modules.keys())))
    await out.msg(self, "modules", chan, [f"loaded: {mods}"])


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
