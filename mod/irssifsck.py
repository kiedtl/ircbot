# if someone says /2/2, respond :)

import common
import time
import random
import re

RESPONSE = ['fuck', 'stahp', 'no u', 'irssi--', 'use weechat', 'you\'re clogging my logs', 'you should try catgirl :^)']
PERCENTAGE = 100

async def filterfsck(self, chan, src, msg):
    if self.is_fsck.match(msg) and src != self.nickname:
        if not chan == '#bots':
            return
        if random.uniform(0, 100) < PERCENTAGE:
            await self.message(chan, random.choice(RESPONSE))

async def init(self):
    self.handle_raw['filterfsck'] = filterfsck
    self.is_fsck = re.compile('^(\/([0-9])+)+$')
