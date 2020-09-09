#
# inspired by pinhook on ~town
#

import common
import handlers
import os
import out
import subprocess
from subprocess import Popen, PIPE, STDOUT


BOTANY_FILE = "/home/%s/.botany/%s_plant.dat"
modname = "botany"


async def visit(self, ch, src, msg, args, opts):
    """
    :name: visit
    :hook: cmd
    :help: let my owner visit your (or someone else's) botany plant on ~team
    :args: @username:str
    """

    # get username
    username = src
    if len(msg) > 1:
        username = msg.split()[0]

    # check if username's botany plant exists
    if username == os.getenv("USER"):
        await out.msg(self, modname, ch, ["I cannot visit myself."])
        return
    if not os.path.isfile(BOTANY_FILE % (username, username)):
        await out.msg(self, modname, ch, [f"I couldn't find {username}'s plant..."])
        return

    # water the plant
    water_string = f"\n4\n{username}\n\nq\n"
    proc = Popen("botany", stdin=PIPE)
    proc.communicate(water_string.encode("utf-8"))
    exit = proc.wait()

    nick_noping = common.nohighlight(username)
    await out.msg(self, modname, ch, [f"I watered {nick_noping}'s plant! ({exit})"])


async def init(self):
    handlers.register(self, modname, visit)
