#
# inspired by pinhook on ~town
#

import common
import dataset
import handlers
import json
import os
import out
import time


VISITORS_FILE = "/home/{}/.botany/visitors.json"
PLANT_FILE = "/home/{}/.botany/{}_plant_data.json"
modname = "botany"

def _plant_desc(username):
    with open(PLANT_FILE.format(username, username)) as finfo:
        return json.load(finfo)['description']

async def visit(self, ch, src, msg, args, opts):
    """
    :name: visit
    :hook: cmd
    :help: water your (or someone else's) botany plant on ~team
    :args: @username:str
    """

    # get username
    username = src
    if len(msg) > 1:
        username = msg.split()[0]
    user_noping = common.nohighlight(username)
    visits_file = VISITORS_FILE.format(username)

    # check if username's botany plant exists
    if not os.path.isfile(visits_file):
        await out.msg(self, modname, ch, [f"I couldn't find {user_noping}'s plant :/ ({visits_file})"])
        return

    # water the plant by adding ourselves to the end of the recipient's
    # visitors.json file in their homedir
    #
    # check if the file is empty before trying to deserialize the JSON in it.
    visitors = []
    if os.stat(visits_file).st_size > 0:
        with open(visits_file) as fvisit:
            visitors = json.load(fvisit)

    # json.load complains if the file object is write-able
    with open(visits_file, 'w') as fwvisit:
        visitors.append({'timestamp': int(time.time()), 'user': self.nickname})
        json.dump(visitors, fwvisit, indent=4)

    description = _plant_desc(username)
    await self.ctcp(ch, "ACTION", f"waters {user_noping}'s {description}!")


async def init(self):
    handlers.register(self, modname, visit)
