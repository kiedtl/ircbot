# backlogger
# stores messages for modules such
# as :pig and :owo

import random, re

async def backlogger(self, c, n, m):
    if m[:len(self.prefix)] == self.prefix:
        return
    if c not in self.backlog:
        self.backlog[c] = []

    self.backlog[c].append([n,m])
    if len(self.backlog[c]) > 1024:
        del self.backlog[c][:-512]

async def init(self):
    self.backlog = {}
    self.raw['backlog'] = backlogger
