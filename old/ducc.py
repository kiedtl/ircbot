import datetime, dataset, math, out, random
from datetime import timedelta
from babel.dates import format_timedelta

modname = "ducc"

# TODO: create helper functions for decreasing or
# increasing health or stress


def ducc_hp_to_str(lvl):
    """ convert health points to string """
    hp_str = {
        # 0 == death
        0: "dying",
        7: "dying",
        14: "very ill",
        35: "ill",
        42: "neglected",
        70: "alright",
        84: "just fine",
        100: "perfectly healthy",
    }

    while not lvl in hp_str:
        lvl -= 1
    return hp_str[lvl]


def ducc_sl_to_str(lvl):
    """ convert stress level to str """
    sl_str = {
        0: "perfectly happy",
        7: "happy",
        14: "a little nervous",
        28: "nervous",
        35: "very nervous",
        48: "a bit stressed",
        56: "very stress out",
        70: "alarmed",
        95: "extremely stressed out",
        100: "nothing",
    }

    while not lvl in sl_str:
        lvl += 1
    return sl_str[lvl]


async def ducc_update_state(self):
    """ update the duccs state """
    cur_state = list(self.ducc_state)[-1]
    new_state = cur_state

    # check CUR_STATE, and see if the ducc was dead
    # if so, just return at this point...
    if not cur_state["alive"]:
        return

    # kay, when was this ducc last fed?
    # if it was last fed more than 14 hours ago,
    # decrease its health by 2 and increase it's stress
    # by 3 for every hour over 14.
    last_fed_unix = int(cur_state["last_fed"])
    last_fed_date = datetime.datetime.fromtimestamp(last_fed_unix)
    hours_since = (datetime.datetime.now() - last_fed_date).seconds / 60 / 60

    if hours_since > 14:
        # oh noes
        hours_over_14 = int(math.floor(hours_since - 14))
        for i in range(0, hours_over_14):
            new_state["health"] -= 2
            new_state["stress"] += 3

    # check the duccs health level. if it's lower
    # than about 45 then increase stress by 15
    # for every 10 HP below 45.
    # oh, and if the duccs health is 0, kill ducc.
    if cur_state["health"] < 45:
        hp_under_45 = 45 - cur_state["health"]
        for i in range(0, int(hp_under_45 / 10)):
            new_state["stress"] += 15

    if cur_state["health"] < 1:
        new_state["alive"] = False

    # now check stress. if it's 100, kill the ducc.
    # even duccs can't live when stressed out
    if cur_state["stress"] > 99:
        new_state["alive"] = False

    # insert NEW_STATE into db, after only after
    # incrementing the id and checking health/stress
    new_state["health"] = max(000, new_state["health"])
    new_state["stress"] = min(100, new_state["stress"])
    new_state["id"] += 1
    self.ducc_state.insert(new_state)


async def ducc_cure(self, c, n, m):
    """ cure the ducc (need admin privs) """
    if not await self.is_admin(n):
        await out.msg(self, modname, c, [f"insufficient privileges"])
        return
    last_state = list(self.ducc_state)[-1]
    self.ducc_state.insert(
        dict(
            last_fed=int(datetime.datetime.now().strftime("%s")),
            health=100,
            stress=0,
            alive=True,
        )
    )
    await out.msg(self, modname, c, [f"done"])


async def ducc_feed(self, c, n, msg):
    """ feed the ducc and increase its health points """
    m = msg.split(" ")

    # check items
    for thing in m:
        if len(thing) < 1:
            await out.msg(self, modname, c, [f"you can't give air!"])
            return

        inv = self.ovendb["inv"]
        its = inv.find_one(name=n, item=thing)

        if its == None:
            await out.msg(
                self, modname, c, [f"you don't have a {thing}! (see :ov inv)"]
            )
            return
        if (
            thing not in self.bakedGoods
            or self.bakedGoods[thing] < 10
            or thing == "ducc"
        ):  # why would a ducc want to eat a ducc??
            await out.msg(self, modname, c, [f"the ducc isn't interested in that..."])
            return

    # delete items
    for thing in m:
        inv.delete(id=its["id"])

    state = list(self.ducc_state)[-1]
    state["health"] += self.bakedGoods[thing] / 10
    state["id"] += 1
    self.ducc_state.insert(state)
    await out.msg(self, modname, c, [f"you fed the ducc!"])


async def ducc_pet(self, c, n, m):
    """ pet the ducc and decrease its stress level """
    state = list(self.ducc_state)[-1]
    state["stress"] -= 10
    state["id"] += 1
    self.ducc_state.insert(state)
    await ducc_quack(self, c, n, m)


async def ducc_quack(self, c, n, m):
    """ QUACK! """
    quacks = ["~quack~", "QUACK!"]
    duccs = ["\_o<", "\_O<", "\_0<", "|\_( o)<"]

    ducc = f"{random.choice(duccs)} {random.choice(quacks)}"
    await out.msg(self, modname, c, [ducc])


async def ducc_shoot(self, c, n, m):
    """ try to kill the ducc :( """
    state = list(self.ducc_state)[-1]
    state["stress"] += 3
    state["id"] += 1
    self.ducc_state.insert(state)

    dodges = True
    if random.uniform(0, 1000) == 666:
        dodges = False
    if dodges:
        await out.msg(self, modname, c, [f"the ducc dodges!"])
    else:
        damage = (
            random.choices(
                population=[10, 30, 50, 70, 90], weights=[0.7, 0.2, 0.05, 0.03, 0.01]
            )
        )[0]

        damages = {
            10: "lightly wounded",
            30: "moderately wounded",
            50: "heavily wounded",
            70: "severely wounded",
            90: "almost dead",
        }

        state = list(self.ducc_state)[-1]
        state["health"] -= damage
        state["id"] += 1
        self.ducc_state.insert(state)

        await out.msg(
            self, modname, c, [f"you shot the ducc! the ducc is {damages[damage]}!"]
        )


async def ducc_info(self, c, n, m):
    """ display health, stress, etc """
    state = list(self.ducc_state)[-1]

    alive = bool(state["alive"])
    health = ducc_hp_to_str(state["health"])
    stress = ducc_sl_to_str(state["stress"])

    last_fed_unix = int(state["last_fed"])
    last_fed_date = datetime.datetime.fromtimestamp(last_fed_unix)
    since = datetime.datetime.now() - last_fed_date
    since_delta_fmt = format_timedelta(since, locale="en_US")

    if not alive:
        await out.msg(self, modname, c, ["the ducc is dead!"])
        return

    await out.msg(
        self,
        modname,
        c,
        [
            f"the ducc is {health} and is feeling {stress}. It was last fed {since_delta_fmt} ago."
        ],
    )


commands = {
    "cure": ducc_cure,
    "feed": ducc_feed,
    "pet": ducc_pet,
    "quack": ducc_quack,
    "shoot": ducc_shoot,
    "info": ducc_info,
}


async def ducc_handle(self, c, src, msg):
    msg = msg.split(" ")
    if len(msg) < 1 or not msg[0] in commands:
        await out.msg(self, modname, c, [self.err_invalid_command])
        return
    await ducc_update_state(self)
    await commands[msg.pop(0)](self, c, src, " ".join(msg))


async def init(self):
    self.duccdb = dataset.connect("sqlite:///dat/ducc.db")
    self.ducc_state = self.duccdb["state"]

    self.cmd["ducc"] = ducc_handle
    self.cmd["du"] = ducc_handle

    self.help["ducc"] = [
        "du[cc] [cmd] - a virtual ducc pet! (very WIP, expect bugs!)",
        "subcommands: cure feed pet quack shoot info",
        "see ':help ducc <command>' for more information.",
    ]
    self.help["du"] = self.help["ducc"]
    self.help["ducc cure"] = ["du[cc] cure - completely cure the ducc (admin only)"]
    self.help["ducc feed"] = [
        "du[cc] feed [item] - feed the ducc <item> from your oven",
        "run ':ov inv' to see what you have in your oven. note that the ducc won't eat inedible items, spam, or other duccs.",
    ]
    self.help["ducc pet"] = [
        "du[cc] pet - pet the ducc. has the effect of lowering its stress level."
    ]
    self.help["ducc quack"] = ["du[cc] quack - \_o< ~quack~"]
    self.help["ducc shoot"] = [
        "du[cc] shoot - try to shoot the ducc; you might end up killing it though."
    ]
    self.help["ducc info"] = ["du[cc] info - show the ducc's state"]
