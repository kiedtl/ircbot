#
# this module was originally written by xfnw.
# (c) xfnw/lickthecheese <xfnw@tilde.team>
#

import config
import handlers
import out

modname = "help"


async def which_module(self, ch, src, msg, args, opts):
    """
    :name: which
    :hook: cmd
    :help: see which module provides a command
    :args: command:str
    :aliases:
    """
    matching_aliases = [k for k, v in self.aliases.items() if msg in v]

    if msg in self.handle_cmd:
        cmd = self.handle_cmd[msg]
        module = self.fndata[cmd]["module"]
        await out.msg(self, modname, ch,
            [f"'{msg}' is a command provided by the {module} module."])
    elif len(matching_aliases) > 0:
        alias_to = matching_aliases[0]
        cmd = self.handle_cmd[alias_to]
        module = self.fndata[cmd]["module"]
        await out.msg(self, modname, ch,
            [f"'{msg}' is an alias to '{alias_to}', a command provided by the {module} module."])
    else:
        await out.msg(self, modname, ch, [f"no such command '{msg}'"])
        return


async def show_commands(self, ch, src, msg, args, opts):
    """
    :name: commands
    :hook: cmd
    :help: show commands for a module
    :args: module:str
    :aliases: cmds
    """
    cmdnames = []
    cmds = [cmd for cmd, func in self.handle_cmd.items()
        if func in self.fndata and self.fndata[self.handle_cmd[cmd]]['module'] == msg]

    commands = ", ".join(cmds)
    await out.msg(self, modname, ch, [f"commands for {msg}: {commands}"])


async def show_help(self, ch, src, msg, args, opts):
    """
    :name: help
    :hook: cmd
    :help: show help for a command
    :args: @command:str
    :aliases: he
    """
    if len(msg) == 0:
        await out.msg(self, modname, ch, [f"Use '{config.prefix}modules' to list modules, '{config.prefix}commands <module>' to list commands, and '{config.prefix}help <command>' to show help for a command."])
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
                    self, modname, ch, [f"no help for '{msg}'; did you mean '{cmd}'?"]
                )
                return

        await out.msg(self, modname, ch, [f"no help for '{msg}'"])


async def init(self):
    handlers.register(self, modname, show_help)
    handlers.register(self, modname, show_commands)
    handlers.register(self, modname, which_module)
