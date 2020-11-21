import configuration
import manager
from manager import *

modname = "pronouns"


@manager.hook(modname, "pronouns", access=AccessType.IDENTIFIED)
@manager.argument("user", optional=True)
@manager.helptext(["see your (or someone else's) preferred pronouns"])
@manager.config("pronouns", ConfigScope.USER, None, None)
async def pronouns(self, chan, nick, msg):
    user = self.users[nick]["account"]

    args = msg.split()
    if len(args) > 0:
        if args[0] in self.users:
            user = self.users[args[0]]["account"]
        else:
            await self.msg(modname, chan, [f"I don't know who {args[0]} is."])
            return

    pronouns = configuration.get(self.network, user, "pronouns")

    if not pronouns:
        await self.msg(modname, chan, [f"no pronouns set for {user}"])
    else:
        await self.msg(modname, chan, [f"pronouns for {user}: {pronouns}"])


async def init(self):
    manager.register(self, pronouns)
