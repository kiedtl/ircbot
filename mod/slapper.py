# On the tilde.chat IRC network, there's a bot named "dustboto"
# that has a ";slap <user>" command. Every time a user is slapped,
# the person that slapped them recieves a random number of
# useless internet points, and the user who was slapped loses that
# many points.
#
# this module reacts everytime someone slaps the bot by slapping back.

import common
import handlers
import time
import re

modname = "slapper"
SLAP_CMD = re.compile(r"^;slap (?P<user>[a-zA-Z0-9]+)$")

# keeps track of the last time a user was slapped
#
# if we slap the same user twice within the same
# 6 hour period, we lose points instead of getting them
slapped = {}


async def handle_slap(self, chan, src, msg):
    """
    :name: filterslap
    :hook: raw
    """
    matches = SLAP_CMD.match(msg)
    if not matches or not matches.groupdict()["user"] == self.nickname:
        # the message was not a slap message, or we were
        # not being slapped
        return

    self.log(modname, f"slapped by {src} in {chan}")

    # track who we slap
    if not src in slapped:
        slapped[src] = 0

    if not slapped[src] + 21600 < time.time():
        # we slapped someone in the last 6 hours. stop.
        return
    else:
        await self.message(chan, f";slap {src}")
        slapped[src] = time.time()


async def init(self):
    handlers.register(self, modname, handle_slap)
