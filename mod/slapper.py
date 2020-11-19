import common
import time
import re


async def handle_slap(self, chan, src, msg):
    self.log(f"[misc] slapped by {src} in {chan}")
    if not src in self.slapped:
        self.slapped[src] = 0
    if not self.slapped[src] + 21600 < time.time():
        return
    else:
        await self.message(chan, f";slap {src}")
        self.slapped[src] = time.time()


async def init(self):
    is_slap = re.compile(f"^;slap " + self.nickname)
    self.handle_reg["slapper"] = (is_slap, handle_slap)

    # keeps track of the last time a user
    # was slapped
    # if we slap the same user twice within
    # the same 6 hour period, we lose points
    # instead of getting them
    self.slapped = {}
