import dataset
import random, re

modname = "karma"
is_karma = re.compile("(^[+-]{2}\(?[\S\W]+\)?$)|(^\(?[\S\W]+\)?[+-]{2}$)")
target_find = re.compile("([+-]{2})?\(?([^()+-]+)\)?([+-]{2})?")


async def handle_karma(self, chan, src, msg):
    lo, target, ro = (target_find.findall(msg))[0]
    op = lo or ro

    # users' shouldn't be able to set
    # their own karma
    if src == target:
        return

    entry = self.karmadb.find_one(name=target)
    if entry == None:
        karma = 0
    else:
        self.karmadb.delete(id=entry["id"])
        karma = entry["amount"]

    if op == "++":
        karma += 1
    elif op == "--":
        karma -= 1

    self.karmadb.insert(dict(name=target, amount=karma))


async def listkarma(self, chan, src, msg):
    entry = self.karmadb.find_one(name=msg)
    if entry == None or entry["amount"] == 0:
        await self.msg(modname, chan, [f"{msg} has 0 karma..."])
    else:
        num = entry["amount"]
        await self.msg(modname, chan, [f"{msg} has {num} karma!"])


async def init(self):
    self.karmadb = dataset.connect("sqlite:///dat/pnts.db")["karma"]

    self.handle_reg["karma"] = (is_karma, handle_karma)
    self.handle_cmd["karma"] = listkarma

    self.help["karma"] = [
        "karma [thing] - get karma for thing. use <thing>++ or ++<thing> to set karma."
    ]
