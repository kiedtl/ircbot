import common
import time
import re

async def filterslap(self, chan, src, msg):
    """detect if message slaps k"""
    if self.is_slap.match(msg) and src != self.nickname:
        print(f'[misc] slapped by {src} in {chan}')
        if not src in self.slapped:
            self.slapped[src] = 0
        if not self.slapped[src] + 21600 < time.time():
            return
        else:
            await self.message(chan, f';slap {src}')
            self.slapped[src] = time.time()

async def init(self):
    self.handle_raw['filterslap'] = filterslap

    # keeps track of the last time a user
    # was slapped
    # if we slap the same user twice within
    # the same 6 hour period, we lose points
    # instead of getting them
    self.slapped = {}

    self.is_slap = re.compile('^;slap\ ' + self.nickname + '$')
