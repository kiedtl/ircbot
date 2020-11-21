import configuration
import manager
import utils
import re
from manager import *

modname = "config"

def _is_oper(self, chan, nick):
    if not chan in self.channels:
        return False

    is_oper = False
    if 'q' in self.channels[chan]:
        is_oper = nick in self.channels[chan]['q']
    if 'o' in self.channels[chan]:
        is_oper = nick in self.channels[chan]['o']

    return is_oper


@manager.hook(modname, "cfg", access=AccessType.IDENTIFIED, aliases=["set"])
@manager.arguments([Arg("context", desc="<user/chan>"), Arg("setting", optional=True), Arg("value", optional=True)])
@manager.helptext(["get, set, or list a configuration value for a user or a channel."])
async def bot_config_set(self, chan, nick, msg):
    user = self.users[nick]['account']

    args = msg.split(" ", 2)
    context_str = args[0]
    setting_str = None
    value = None

    if len(args) > 1:
        setting_str = args[1]
    if len(args) > 2:
        value = args[2]

    ctxtype = None

    ctxchar = context_str[0]
    if ctxchar == 'c':
        ctxtype = ConfigScope.CHAN
        ctxname = chan
    elif ctxchar == 'u':
        ctxtype = ConfigScope.USER
        ctxname = user
    else:
        await self.msg(modname, chan, [f"invalid context '{context_str}'. Valid contexts: 'user' or 'channel'."])
        return

    # build a list of all exported values.
    exported = [data["configs"] for fn,data in self.fndata.items() if "configs" in data]
    exported = [conf for conf in utils.flatten(exported) if conf[1] == ctxtype]
    exported_names = [conf[0] for conf in exported]

    # if no setting is given, then list all settings for context.
    if not setting_str:
        await self.msg(modname, chan, ["settings: {}".format(", ".join(exported_names))])
        return

    # is the setting we're trying to get/set a recognized, exported configuration value?
    if not setting_str in exported_names:
        await self.msg(modname, chan, [f"no such setting '{setting_str}'."])
        return

    # if no value is given, print out the current value for the setting.
    if not value:
        cur_value = configuration.get(self.network, ctxname, setting_str, default="")
        await self.msg(modname, chan, [f"current value for '{setting_str}': '{cur_value}'"])
        return

    setting = [s for s in exported if s[0] == setting_str][0]

    # don't let users change settings for channels they don't have +o in.
    if ctxtype == ConfigScope.CHAN and not _is_oper(self, ctxname, nick):
        await self.msg(modname, chan, [f"you may not change settings for channels that you do not have +o in."])
        return

    # ensure the value given is valid.
    pattern = setting[2]
    description = setting[3]

    if pattern and not re.match(pattern, value):
        if description:
            await self.msg(modname, chan, [f"invalid value format. format: {description}"])
        else:
            await self.msg(modname, chan, [f"invalid value format."])
        return

    # now we can set the value
    # NOTE: user pings are allowed intentionally
    configuration.set(self.network, ctxname, setting[0], value)
    await self.msg(modname, chan, [f"set '{setting[0]}' for '{ctxname}' to '{value}'"])


async def init(self):
    manager.register(self, bot_config_set)
