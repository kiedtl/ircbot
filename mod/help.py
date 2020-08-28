#
# this module was originally written by xfnw.
# (c) xfnw/lickthecheese <xfnw@tilde.team>
#

import handlers
import out

modname = "help"


async def show_help(self, ch, src, msg, args, opts):
    """
    :name: help
    :hook: cmd
    :help: list commands or show help on command
    :args: @command:str
    :aliases: h he
    """

    # list commands if no arguments
    if len(msg) < 1:
        cmdnames = []

        commands = ", ".join(self.handle_cmd)
        await out.msg(self, modname, ch, [f"commands: {commands}"])
        return

    # list of aliases that might match command
    aliases = {k for k, v in self.aliases.items() if msg in v}

    if msg in self.help:
        await out.msg(self, modname, ch, self.help[msg])
    elif len(aliases) > 0:
        a = list(aliases)[0]
        await out.msg(self, modname, ch, self.help[a])
    else:
        # fuzzy search when all else fails
        # TODO: fuzzy search aliases
        for cmd in sorted(self.handle_cmd.keys()):
            if cmd.startswith(msg):
                await out.msg(
                    self, modname, ch, [f"no help for '{msg}', did you mean '{cmd}'?"]
                )
                return

        await out.msg(self, modname, ch, [f"no help for '{msg}'"])


async def init(self):
    handlers.register(self, modname, show_help)
