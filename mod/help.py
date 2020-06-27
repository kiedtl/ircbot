from common import modname

async def helpParse(self, c, n, m):
    if m in self.help:
        if len(self.help[m]) > 1:
            self.more[c] = self.help[m][1]
        await self.message(c, '{} {}'
            .format(modname('help'), self.help[m][0]))
    else:
        await self.message(c, '{} commands: {}'
            .format(modname('help'),
                ' '.join([i for i in self.help if not ' ' in i])))

async def more(self, c, n, m):
    if c in self.more:
        await self.message(c, '{} {}'
            .format(modname('help'), self.more.pop(c)))
        return
    else:
        await self.message(c, '{} no more text to show'
            .format(modname('help')))


async def init(self):
    self.cmd['help'] = helpParse
    self.cmd['more'] = more
    self.help['help'] = ['help command - list commands or show help on command']
    self.help['help command'] = ['help <command> - show more info about a command']
    self.help['more'] = ['more - view more text']
    self.more = {}
