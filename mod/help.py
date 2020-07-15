import handlers
import out

modname = 'help'

async def show_help(self, c, n, m):
    '''
    :name: help
    :hook: cmd
    :help: list commands or show help on command
    :args: @command:str
    :aliases: h he
    '''

    # list commands if no arguments
    if len(m) < 1:
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

    # list of aliases that might match command
    aliases = {k for k, v in self.aliases.items() if m in v}

    if m in self.help:
        await out.msg(self, modname, c, self.help[m])
    elif len(aliases) > 0:
        a = list(aliases)[0]
        await out.msg(self, modname, c, self.help[a])
    else:
        # fuzzy search when all else fails
        # TODO: fuzzy search aliases
        for cmd in sorted(self.handle_cmd.keys()):
            if cmd.startswith(m):
                await out.msg(self, modname, c,
                    [f'no help for \'{m}\', did you mean \'{cmd}\'?'])
                return

        await out.msg(self, modname, c, [f'no help for \'{m}\''])

async def more(self, c, n, m):
    '''
    :name: more
    :hook: cmd
    :help: view more text
    :args:
    :aliases: m
    '''

    # TODO: move to separate module
    await out.more(self, c)

async def init(self):
    handlers.register(self, modname, show_help)
    handlers.register(self, modname, more)
