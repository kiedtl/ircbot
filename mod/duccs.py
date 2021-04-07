# [TODO] If a ducc has flown through a channel MAX_FLIGHT times, remove the ducc.
# [DONE] :duccs/:friends/:enemies/:duccstats command that allows users to see
#        their duccs
# [DONE] make duck statistics persist in a database
# [DONE] set ducc owners to user's account name, not nickname
# [DONE] do not ping nicknames/users

import configuration
import dataclasses
import dataset
import fmt
import inflect
import manager
import random
import time
import utils

from manager import *
from handlers import *
from typing import Tuple

modname = "duccs"

MSGS_UNTIL_DUCC = 110
FLIGHTS_UNTIL_DELETION = 10
CHANCE_OF_DUCC = 25
SLOGANS = [
    "QUACK!",
    "QUACK QUACK!",
    "QUACK! QUACK!",
    "FLAP!",
    "FLAP FLAP!",
    "*quack*",
    "*flap*",
]
SINGLE_WAVE_LEN = 8
WAVES = "・゜゜・。。・゜゜・。。・゜゜・。。・゜゜"
REQUIRE_MAGIC_FOR = 60

duccs = {}
inflect_ngn = inflect.engine()
ducc_countdown = {}
db = dataset.connect("sqlite:///dat/data.db")
ducc_db = db["duccs"]


def _format_items(items, sort=lambda i: i[1], itemmap=lambda i: i):
    """
    Take an array of items and return a string with each item
    and the number of times it occurs in the array.

    Example: ['a', 'a', 'b', 'z', 'z'] => "a (×2), z (×1), b (×1)
    """
    itemstats = {}
    for i in items:
        if not i in itemstats:
            itemstats[i] = 0
        itemstats[i] += 1

    fmtd = []
    for i in sorted(itemstats.items(), key=sort, reverse=True):
        i = (itemmap(i[0]), i[1])
        fmtd.append(f"{i[0]} (×{i[1]})")

    return ", ".join(fmtd)


@dataclasses.dataclass
class Ducc:
    # time at which the ducc appeared
    appeared: int

    # the "magic number" needed to befriend/kill a ducc. It must appear
    # after the "bef" or "bang" commands, e.g. "bef 45", unless the ducc
    # is older than about 1 minute
    #
    # structure: Tuple[<answer>, <question>]
    magic: Tuple[str, str]

    # unique per ducc
    waves: str
    art: str
    slogan: str

    # number of times ducc appeared in channel.
    # if a ducc is not befriended after MSGS_UNTIL_DUCCS,
    # the ducc reappears... unless flew_threw > FLIGHTS_UNTIL_DELETION.
    flew_through: int = 0

    # free: has the ducc been befriended/shot yet?
    # captive_since: when was the ducc befriended?
    free: bool = True
    captive_since: int = 0

    is_phantom: bool = False


def _ducc_persist(network, chan, src, was_killed, ducc: Ducc):
    ducc_db.insert(
        dict(
            network=network,
            channel=chan,
            appeared=ducc.appeared,
            captured=ducc.captive_since,
            flew_through=ducc.flew_through,
            was_killed=was_killed,
            owner=src,
        )
    )


def _ducc_fmt(ducc: Ducc):
    art = fmt.bold(ducc.art)

    if not ducc.magic[1] == "":
        magic = fmt.yellow(ducc.magic[1])
        magic = f"[{magic}]"
    else:
        magic = ""

    return f"{ducc.waves} {art} {ducc.slogan}  {magic}"


def _ducc_ascii():
    r_beak = random.choice(["<", "⁖", "-"])
    l_beak = random.choice([">", "-"])
    r_tail = random.choice(["\\\\", "\\"])
    l_tail = random.choice(["//", "/"])
    head = random.choice([h for h in "oðõôòóö"])

    return random.choice([f"{r_tail}_{head}{r_beak}", f"{l_beak}{head}_{l_tail}"])


def _ducc_waves():
    index = round(random.uniform(0, (len(WAVES) - SINGLE_WAVE_LEN) - 1))
    return WAVES[index : (index + SINGLE_WAVE_LEN)]


def _ducc_math_magic():
    num2 = round(random.uniform(1, 5))
    num1 = round(random.uniform(5, 10))
    operator = random.choice(["+", "-", "*"])

    num1_str = inflect_ngn.number_to_words(num1)
    num2_str = inflect_ngn.number_to_words(num2)

    magic = 0
    operator_str = ""
    if operator == "+":
        operator_str = random.choice(["+", "plus", "added to"])
        magic = num1 + num2
    elif operator == "-":
        operator_str = random.choice(["-", "minus"])
        magic = num1 - num2
    elif operator == "*":
        operator_str = random.choice(["*", "times", "multiplied by", "×"])
        magic = num1 * num2

    magic_str = f"{num1_str} {operator_str} {num2_str}"
    return (str(magic), magic_str)


def _ducc_random_magic():
    magic = round(random.uniform(10, 99))
    return (str(magic), str(magic))


def _ducc_none_magic():
    return ("", "")


async def _summon_ducc(self, chan, phantom):
    if not chan in duccs:
        duccs[chan] = []

    # don't create new duccs if there's still a ducc that
    # hasn't been befriended
    if len(duccs[chan]) > 0 and duccs[chan][-1].free:
        duccs[chan][-1].flew_through += 1
        await self.message(chan, _ducc_fmt(duccs[chan][-1]))
        return

    _scii = _ducc_ascii()
    slogan = random.choice(SLOGANS)
    waves = _ducc_waves()
    magic = random.choice([_ducc_math_magic, _ducc_random_magic, _ducc_none_magic])()

    ducc = Ducc(
        appeared=time.time(),
        magic=magic,
        waves=waves,
        art=_scii,
        slogan=slogan,
        is_phantom=phantom,
    )
    duccs[chan].append(ducc)
    await self.message(chan, _ducc_fmt(ducc))


@manager.hook(modname, "filterducc", hook=HookType.RAW)
@manager.config("ducchunt", ConfigScope.CHAN, desc="True or False", cast=bool)
async def filterducc(self, chan, src, msg):
    if src == self.nickname:
        return

    enabled = configuration.get(self.network, chan, "ducchunt", cast=bool)
    if not enabled:
        return

    if not chan in ducc_countdown:
        ducc_countdown[chan] = MSGS_UNTIL_DUCC

    ducc_countdown[chan] -= 1
    if ducc_countdown[chan] <= 0:
        if random.uniform(1, 100) < CHANCE_OF_DUCC:
            await _summon_ducc(self, chan, False)
            ducc_countdown[chan] = MSGS_UNTIL_DUCC


@manager.hook(modname, "mkducc", access=AccessType.ADMIN)
@manager.helptext(["summon a ducc for debugging purposes"])
async def summon(self, chan, src, msg):
    if not chan in ducc_countdown:
        ducc_countdown[chan] = MSGS_UNTIL_DUCC

    ducc_countdown[chan] -= 1
    if ducc_countdown[chan] <= 0:
        ducc_countdown[chan] = MSGS_UNTIL_DUCC
    await _summon_ducc(self, chan, True)


@manager.hook(modname, "lsducc", access=AccessType.ADMIN)
@manager.arguments([Arg("channel", optional=True)])
@manager.helptext(["see how many messages are left until a ducc will appear"])
async def ls(self, chan, src, msg):
    channel = chan
    if len(msg) > 0:
        channel = msg

    until = "unknown"
    if channel in ducc_countdown:
        until = ducc_countdown[channel]

    return (Msg.OK, f"{until}")


async def _catches_ducc(self, chan, src, msg):
    if not chan in duccs or len(duccs[chan]) == 0:
        await self.msg(modname, chan, [f"{src}: There was no ducc!"])
        return False

    if not duccs[chan][-1].free:
        missed = time.time() - duccs[chan][-1].captive_since
        await self.msg(
            modname, chan, [f"{src} missed the duck by {missed:,.2f} seconds!"]
        )
        return False

    if duccs[chan][-1].is_phantom:
        await self.msg(modname, chan, [f"WHOOSH! the ducc vanishes into thin air!"])
        return False

    if msg != duccs[chan][-1].magic[0]:
        if duccs[chan][-1].appeared + REQUIRE_MAGIC_FOR > time.time():
            await self.msg(modname, chan, [f"FLAP! {src} misses the ducc!"])
            return False

    return True


async def _catch_ducc(self, chan, src, was_killed: bool):
    user = src
    if user in self.users and self.users[user]["identified"]:
        user = self.users[user]["account"]

    duccs[chan][-1].free = False
    duccs[chan][-1].captive_since = time.time()
    _ducc_persist(self.network, chan, user, was_killed, duccs[chan][-1])


@manager.hook(modname, "befr", aliases=["bef"])
@manager.arguments([Arg("magic", desc="<ducc-code>", optional=True)])
@manager.helptext(["befriend a ducc"])
async def befriend(self, chan, src, msg):
    if await _catches_ducc(self, chan, src, msg):
        befd_in = time.time() - duccs[chan][-1].appeared
        await _catch_ducc(self, chan, src, False)
        await self.msg(
            modname,
            chan,
            [f"QUACK! {src} befriended the ducc in {befd_in:,.2f} seconds!"],
        )


@manager.hook(modname, "bang", aliases=["bash", "trap"])
@manager.arguments([Arg("magic", desc="<ducc-code>", optional=True)])
@manager.helptext(["shoot a ducc"])
async def bang(self, chan, src, msg):
    if await _catches_ducc(self, chan, src, msg):
        death_cry_aas = "A" * round(random.uniform(1, 3))
        death_cry = f"QU{death_cry_aas}CK!"

        murdered_in = time.time() - duccs[chan][-1].appeared
        await _catch_ducc(self, chan, src, True)
        await self.msg(
            modname,
            chan,
            [
                f"{death_cry} {src} brutally murdered the ducc in {murdered_in:,.2f} seconds!"
            ],
        )


@manager.hook(modname, "friends", aliases=["frens"])
@manager.arguments([Arg("channel", optional=True)])
@manager.helptext(["see all ducc friends for a channel"])
async def friends(self, chan, src, msg):
    channel = chan
    if len(msg) > 1:
        channel = msg

    chan_duccs = ducc_db.find(channel=channel, was_killed=False)
    owners = [ducc["owner"] for ducc in chan_duccs]
    formatted = _format_items(owners, itemmap=lambda i: fmt.zwnj(i))
    await self.msg(modname, chan, [f"ducc friends in {chan}: {formatted}"])


@manager.hook(modname, "enemies", aliases=["fiends"])
@manager.arguments([Arg("channel", optional=True)])
@manager.helptext(["see all ducc enemies for a channel"])
async def fiends(self, chan, src, msg):
    channel = chan
    if len(msg) > 1:
        channel = msg

    chan_duccs = ducc_db.find(channel=channel, was_killed=True)
    owners = [ducc["owner"] for ducc in chan_duccs]
    formatted = _format_items(owners, itemmap=lambda i: fmt.zwnj(i))
    await self.msg(modname, chan, [f"ducc enemies in {chan}: {formatted}"])


async def _user_duckstats(self, chan, user):
    user_noping = fmt.zwnj(user)
    ducc_record = list(ducc_db.find(owner=user))
    total = len(ducc_record)
    channels = _format_items([ducc["channel"] for ducc in ducc_record])

    if total == 0:
        await self.msg(modname, chan, [f"{user} doesn't have any duccs!"])
        return

    befriended = len([ducc for ducc in ducc_record if ducc["was_killed"] == False])
    murdered = len([ducc for ducc in ducc_record if ducc["was_killed"] == True])
    times = sorted([ducc["captured"] - ducc["appeared"] for ducc in ducc_record])
    fastest = times[0]
    slowest = times[-1]

    # Only calculate the average captures of captures done in less than 4 seconds.
    fast_times = [time for time in times if time <= 4]
    average = sum(fast_times) / len(fast_times)

    befriended_str = fmt.bold(fmt.green(befriended))
    murdered_str = fmt.bold(fmt.red(murdered))

    first_message = ""
    if total == 1:
        first_message = f"{user_noping} has captured {total} duccs, befriending {befriended_str} and murdering {murdered_str}."
    else:
        first_message = f"{user_noping} has captured {total} duccs, befriending {befriended_str} and murdering {murdered_str}. Their fastest capture was {fastest:,.2f} seconds, and their slowest capture was {slowest:,.2f} seconds; on average, they capture duccs in about {average:,.2f} seconds."

    await self.msg(
        modname, chan, [first_message, f"{user_noping} has duccs in: {channels}"]
    )


async def _chan_duckstats(self, chan, context):
    ducc_record = list(ducc_db.find(channel=context))
    total = len(ducc_record)

    if total == 0:
        await self.msg(modname, chan, [f"no duccs were in {context}!"])
        return

    befriended = len([ducc for ducc in ducc_record if ducc["was_killed"] == False])
    murdered = len([ducc for ducc in ducc_record if ducc["was_killed"] == True])
    times = sorted(
        [(ducc["captured"] - ducc["appeared"], ducc["owner"]) for ducc in ducc_record],
        key=lambda i: i[0],
    )
    fastest = times[0]
    slowest = times[-1]

    # Only calculate the average captures of captures done in less than 4 seconds.
    fast_times = [time[0] for time in times if time[0] <= 4]
    average = sum(fast_times) / len(fast_times)

    befriended_str = fmt.bold(fmt.green(befriended))
    murdered_str = fmt.bold(fmt.red(murdered))
    fastest_user_str = fmt.blue(fmt.zwnj(fastest[1]))
    slowest_user_str = fmt.blue(fmt.zwnj(slowest[1]))

    await self.msg(
        modname,
        chan,
        [
            f"duck stats for {context}: {befriended_str} befriended, {murdered_str} murdered. The fastest capture was by {fastest_user_str} in {fastest[0]:,.2f}; the slowest capture was by {slowest_user_str} in {slowest[0]:,.2f}. The average speed of a ducc capture is {average:,.2f} seconds."
        ],
    )


async def _all_duckstats(self, chan):
    ducc_record = list(ducc_db.find())
    total = len(ducc_record)

    channels = [ducc["channel"] for ducc in ducc_record]
    channels_total = len(utils.dedup(channels))

    channel_frens = [
        ducc["channel"] for ducc in ducc_record if ducc["was_killed"] == False
    ]
    channel_foes = [
        ducc["channel"] for ducc in ducc_record if ducc["was_killed"] == True
    ]

    befriended = len([ducc for ducc in ducc_record if ducc["was_killed"] == False])
    murdered = len([ducc for ducc in ducc_record if ducc["was_killed"] == True])

    times = sorted(
        [
            (ducc["captured"] - ducc["appeared"], ducc["owner"], ducc["channel"])
            for ducc in ducc_record
        ],
        key=lambda i: i[0],
    )
    fastest = times[0]
    slowest = times[-1]
    average = sum([t[0] for t in times]) / len(times)

    befriended_str = fmt.bold(fmt.green(befriended))
    murdered_str = fmt.bold(fmt.red(murdered))
    total_str = fmt.bold(fmt.cyan(total))
    channels_total_str = fmt.yellow(channels_total)
    channels_str = _format_items(channels)
    fastest_user_str = fmt.blue(fmt.zwnj(fastest[1]))
    slowest_user_str = fmt.blue(fmt.zwnj(slowest[1]))

    await self.msg(
        modname,
        chan,
        [
            f"duck stats for {channels_total_str} channels: {befriended_str} befriended, {murdered_str} murdered, {total_str} total. Fastest capture was {fastest[0]:,.2f} by {fastest_user_str} in {fastest[2]}; slowest was {slowest[0]:,.2f} by {slowest_user_str} in {slowest[2]}.",
            f"top channels: {channels_str}",
        ],
    )


@manager.hook(modname, "duckstats")
@manager.arguments([Arg("context", desc="<user/channel>", optional=True)])
@manager.helptext(["see ducc statistics for a channel or a user"])
async def duckstats(self, chan, src, msg):
    context = src
    args = msg.split(" ")
    if len(msg) > 0:
        context = msg

    if context[0] == "#":
        await _chan_duckstats(self, chan, context)
    elif context == "*":
        await _all_duckstats(self, chan)
    else:
        await _user_duckstats(self, chan, context)


async def init(self):
    manager.register(self, filterducc)
    manager.register(self, summon)
    manager.register(self, ls)
    manager.register(self, befriend)
    manager.register(self, bang)
    manager.register(self, friends)
    manager.register(self, fiends)
    manager.register(self, duckstats)
