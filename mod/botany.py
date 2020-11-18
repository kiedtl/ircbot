#
# inspired by pinhook on ~town
#

import common
import dataset
import handlers
import json
import math
import os
import out
import re
import time

from datetime import datetime, timedelta
from babel.dates import format_timedelta

VISITORS_FILE = "/home/{}/.botany/visitors.json"
PLANT_FILE = "/home/{}/.botany/{}_plant_data.json"
AGE_RE = re.compile(r"(?P<days>\d+)d:(?P<hours>\d+)h:(?P<minutes>\d+)m:(?P<seconds>\d+)s")

modname = "botany"

def _plant_visitors(username):
    visits_file = VISITORS_FILE.format(username)
    # check if the file is empty before trying to deserialize
    # the JSON in it.
    if os.stat(visits_file).st_size > 0:
        with open(visits_file) as fvisit:
            return json.load(fvisit)
    else:
        return []

def _plant_info(username):
    with open(PLANT_FILE.format(username, username)) as finfo:
        return json.load(finfo)

async def botany(self, ch, src, msg, args, opts):
    """
    :name: botany
    :hook: cmd
    :help: check on your (or someone else's) botany plant
    :args: @username:str
    """
    username = src
    if len(msg) > 1:
        username = msg.split()[0]
    user_noping = common.nohighlight(username)

    info = {}
    visitors = []

    try:
        info = _plant_info(username)
        visitors = _plant_visitors(username)
    except FileNotFoundError:
        await out.msg(self, modname, ch, [f"I couldn't find {user_noping}'s plant :/"])
        return

    description = info['description']
    info_watered_on = datetime.utcfromtimestamp(info['last_watered'])
    generation = info['generation']
    score = math.ceil(info['score'])

    # the age string may have fields where the value is only one digit.
    # fix this with a regex to make it palatable to datetime.strptime.
    age_fields = AGE_RE.match(info["age"]).groupdict()
    age_fields2 = {}
    for (name, param) in age_fields.items():
        if param:
            age_fields2[name] = int(param)
    age_delta = timedelta(**age_fields2)

    # when a user is visited, the info file isn't updated; instead, the visitor
    # and visit timestamp is stored in visitors.json. We need to check both of
    # these files (the info file and visitors.json) to find the last time the plant
    # was watered.
    last_visit = datetime.utcfromtimestamp(0)
    last_visitor = None

    if len(visitors) > 0:
        last_visit = datetime.utcfromtimestamp(visitors[-1]['timestamp'])
        last_visitor = visitors[-1]['user']

    if info_watered_on > last_visit:
        watered_on = info_watered_on
    else:
        watered_on = last_visit

    watered_by_str = ""
    if not last_visitor == None:
        last_visitor_noping = common.nohighlight(last_visitor)
        watered_by_str = f" by {last_visitor_noping}"

    last_watered = datetime.now() - watered_on
    str_last_watered = format_timedelta(last_watered, locale="en_US")
    str_age = format_timedelta(age_delta, locale="en_US")

    is_dead = False
    if info['is_dead'] or last_watered.days >= 5:
        is_dead = True

    if is_dead:
        await out.msg(self, modname, ch, [f"{user_noping}'s {description} is dead!"])
    else:
        await out.msg(self, modname, ch, [f"{user_noping}'s {description} was last watered {str_last_watered} ago{watered_by_str}. It has {score:,} points, is {str_age} old, and is on generation {generation}."])

async def visit(self, ch, src, msg, args, opts):
    """
    :name: visit
    :hook: cmd
    :help: water your (or someone else's) botany plant
    :args: @username:str
    """

    username = src
    if len(msg) > 1:
        username = msg.split()[0]
    user_noping = common.nohighlight(username)

    visits_file = VISITORS_FILE.format(username)
    info = {}

    # water the plant by adding ourselves to the end of the recipient's
    # visitors.json file in their homedir
    visitors = []

    try:
        info = _plant_info(username)
        visitors = _plant_visitors(username)
    except FileNotFoundError:
        await out.msg(self, modname, ch, [f"I couldn't find {user_noping}'s plant :/"])
        return

    is_dead = info['is_dead']
    description = info['description']

    # don't bother watering dead plants
    if is_dead:
        await self.ctcp(ch, "ACTION", f"gazes sadly at {user_noping}'s dead {description}")
        return

    # just add ourselves to the visitors list. botany will take care of the
    # rest the next time that user opens it.
    visitors.append({'timestamp': int(time.time()), 'user': self.nickname})

    # json.load complains if the file object is write-able
    try:
        with open(visits_file, 'w') as fwvisit:
            json.dump(visitors, fwvisit, indent=4)
            await self.ctcp(ch, "ACTION", f"waters {user_noping}'s {description}!")
    except PermissionError:
        await self.ctcp(ch, "ACTION", f"peeks at {user_noping}'s {description} over their garden wall")


async def init(self):
    handlers.register(self, modname, visit)
    handlers.register(self, modname, botany)
