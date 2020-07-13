import out
modname = 'help'

async def helpParse(self, c, n, m):
    aliases = {k for k, v in self.aliases.items() if m in v}

    if m in self.help:
        await out.msg(self, modname, c, self.help[m])
    elif len(aliases) > 0:
        a = list(aliases)[0]
        await out.msg(self, modname, c, self.help[a])
    else:
        cmdnames = []
        # we want to display aliases for commands, too!
        for cmd in sorted(self.handle_cmd):
            aliases = {k for k, v in self.aliases.items() if cmd in k}
            if len(aliases) > 0:
                suff = '/'.join(self.aliases[list(aliases)[0]])
                cmdnames.append(cmd + '/' + suff)
            else:
                cmdnames.append(cmd)

        commands = ', '.join(cmdnames)
        await out.msg(self, modname, c,
            [f'commands: {commands}'])

async def more(self, c, n, m):
    # TODO: move to separate module
    await out.more(self, c)

async def init(self):
    self.handle_cmd['help'] = helpParse
    self.handle_cmd['more'] = more

    self.help['help'] = ['help [command] - list commands or show help on command']
    self.help['more'] = ['more - view more text']
