import out
modname = 'help'

async def helpParse(self, c, n, m):
    if m in self.help:
        await out.msg(self, modname, c, self.help[m])
    else:
        commands = ', '.join(
            [cmd for cmd in sorted(self.cmd) if not ' ' in cmd])
        await out.msg(self, modname, c,
            [f'commands: {commands}'])

async def more(self, c, n, m):
    # TODO: move to separate module
    await out.more(self, c)

async def init(self):
    self.cmd['help'] = helpParse
    self.cmd['more'] = more
    self.help['help'] = ['help command - list commands or show help on command']
    self.help['help command'] = ['help <command> - show more info about a command']
    self.help['more'] = ['more - view more text']
    self.more = {}
