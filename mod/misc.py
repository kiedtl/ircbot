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
    response = ""

    owner = common.nohighlight(config.botmaster)
    response += f"I'm {self.nickname}! | owner: {owner} "

    if not config.upstream == None:
        source = "".join([common.nohighlight(i) for i in config.upstream])
        response += f"| source: {source} "

    email = common.nohighlight(config.email[0]) + "‍＠‍" + config.email[1]
    response += f"| contact: {email} | usage: try {config.prefix}help"
    await out.msg(self, "who", chan, [response])


async def init(self):
    self.handle_cmd["modules"] = list_mods
    self.handle_cmd["ping"] = ping
    self.handle_cmd["who"] = whoami

    self.help["modules"] = ["modules - list loaded modules"]
    self.help["ping"] = ["ping - check if I'm responding"]
    self.help["who"] = ["who - get information about my owner"]
