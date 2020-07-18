import handlers
import out

modname = 'help'

async def show_help(self, ch, src, msg, args, opts):
    '''
    :name: help
    :hook: cmd
    :help: list commands or show help on command
    :args: @command:str
    :aliases: h he
    '''

    # list commands if no arguments
    if len(args) < 1:
        cmdnames = []
        # we want to display aliases for commands, too!
        #for cmd in sorted(self.handle_cmd):
        #    aliases = {k for k, v in self.aliases.items() if cmd in k}
        #    if len(aliases) > 0:
        #        suff = '/'.join(self.aliases[list(aliases)[0]])
        #        cmdnames.append(cmd + '/' + suff)
        #    else:
        #        cmdnames.append(cmd)

        commands = ', '.join(self.handle_cmd)
        await out.msg(self, modname, ch,
            [f'commands: {commands}'])
        return

    # list of aliases that might match command
    aliases = {k for k, v in self.aliases.items() if m in v}

    if m in self.help:
        await out.msg(self, modname, ch, self.help[msg])
    elif len(aliases) > 0:
        a = list(aliases)[0]
        await out.msg(self, modname, ch, self.help[a])
    else:
        # fuzzy search when all else fails
        # TODO: fuzzy search aliases
        for cmd in sorted(self.handle_cmd.keys()):
            if cmd.startswith(msg):
                await out.msg(self, modname, ch,
                    [f'no help for \'{msg}\', did you mean \'{cmd}\'?'])
                return

        await out.msg(self, modname, ch, [f'no help for \'{msg}\''])

async def more(self, ch, src, msg, args, opts):
    '''
    :name: more
    :hook: cmd
    :help: view more text
    :args:
    :aliases: m
    '''

    # TODO: move to separate module
    await out.more(self, ch)

async def init(self):
    handlers.register(self, modname, show_help)
    handlers.register(self, modname, more)
