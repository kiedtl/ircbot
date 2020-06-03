async def helpParse(self, c, n, m):
    if m in self.help:
        self.more[c] = self.help[m][1]
        await self.message(c, '[HELP] {}'.format(self.help[m][0]))
    else:
        await self.message(c, '[HELP] commands: {}'
                .format(' '.join([i for i in self.help if not ' ' in i])))

async def more(self, c, n, m):
    if c in self.more:
        await self.message(c, '[HELP] {}'.format(self.more.pop(c)))
        return
    else:
        await self.message(c, '[HELP] no more text to show')


async def init(self):
    self.cmd['help'] = helpParse
    self.cmd['more'] = more
    self.help['help'] = ['help command - list commands or show help on command']
    self.help['help command'] = ['help <command> - show more info about a command']
    self.help['more'] = ['more - view more text']
    self.more = {}
