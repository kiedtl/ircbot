#
# this module was originally written by xfnw.
# (c) xfnw/lickthecheese <xfnw@tilde.team>
#

import config
import handlers

modname = "help"


async def show_modules(self, chan, src, msg):
    """
    :name: modules
    :hook: cmd
    :help: list loaded modules
    :args:
    :aliases:
    """
    mods = ", ".join(sorted(list(self.modules.keys())))
    await self.msg(modname, chan, [f"loaded: {mods}"])

async def which_module(self, ch, src, msg):
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
        await self.msg(
            modname, ch, [f"'{msg}' is a command provided by the {module} module."]
        )
    elif len(matching_aliases) > 0:
        alias_to = matching_aliases[0]
        cmd = self.handle_cmd[alias_to]
        module = self.fndata[cmd]["module"]
        await self.msg(
            modname,
            ch,
            [
                f"'{msg}' is an alias to '{alias_to}', a command provided by the {module} module."
            ],
        )
    else:
        await self.msg(modname, ch, [f"no such command '{msg}'"])
        return


async def show_commands(self, ch, src, msg):
    """
    :name: commands
    :hook: cmd
    :help: show commands for a module
    :args: module:str
    :aliases: cmds
    """
    cmdnames = []
    cmds = [
        cmd
        for cmd, func in self.handle_cmd.items()
        if func in self.fndata and self.fndata[self.handle_cmd[cmd]]["module"] == msg
    ]

    commands = ", ".join(cmds)
    await self.msg(modname, ch, [f"commands for {msg}: {commands}"])


async def show_help(self, ch, src, msg):
    """
    :name: help
    :hook: cmd
    :help: show help for a command
    :args: @command:str
    :aliases: he
    """
    if len(msg) == 0:
        await self.msg(
            modname,
            ch,
            [
                f"Use '{config.prefix}modules' to list modules, '{config.prefix}commands <module>' to list commands, and '{config.prefix}help <command>' to show help for a command."
            ],
        )
        return

    # list of aliases that might match command
    aliases = {k for k, v in self.aliases.items() if msg in v}

    if msg in self.help:
        await self.msg(modname, ch, self.help[msg])
    elif len(aliases) > 0:
        a = list(aliases)[0]
        await self.msg(modname, ch, self.help[a])
    else:
        # fuzzy search when all else fails
        # TODO: fuzzy search aliases
        for cmd in sorted(self.handle_cmd.keys()):
            if cmd.startswith(msg):
                await self.msg(
                    modname, ch, [f"no help for '{msg}'; did you mean '{cmd}'?"]
                )
                return

        await self.msg(modname, ch, [f"no help for '{msg}'"])


async def init(self):
    handlers.register(self, modname, show_help)
    handlers.register(self, modname, show_commands)
    handlers.register(self, modname, show_modules)
    handlers.register(self, modname, which_module)
