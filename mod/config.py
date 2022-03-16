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
    if "q" in self.channels[chan]["modes"]:
        is_oper = nick in self.channels[chan]["modes"]["q"]
    if "o" in self.channels[chan]:
        is_oper = nick in self.channels[chan]["modes"]["o"]

    return is_oper


@manager.hook(modname, "cfg", access=AccessType.IDENTIFIED)
@manager.arguments(
    [
        Arg("context", desc="<user/chan>"),
        Arg("setting", optional=True),
        Arg("value", optional=True),
    ]
)
@manager.helptext(["get, set, or list a configuration value for a user or a channel."])
async def bot_config_set(self, chan, nick, msg):
    user = self.users[nick]["account"]

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
    if ctxchar == "c":
        ctxtype = ConfigScope.CHAN
        ctxname = chan
    elif ctxchar == "u":
        ctxtype = ConfigScope.USER
        ctxname = user
    else:
        await self.msg(
            modname,
            chan,
            [f"invalid context '{context_str}'. Valid contexts: 'user' or 'channel'."],
        )
        return

    # allow for viewing/setting configs for other users/chans
    ctxargs = context_str.split(":")
    if len(ctxargs) > 1:
        ctxname = ctxargs[1]
        if (
            ctxtype == ConfigScope.USER
            and ctxname in self.users
            and self.users[ctxname]["identified"]
        ):
            ctxname = self.users[ctxname]["account"]

    # build a list of all exported values.
    exported = [
        data["configs"] for fn, data in self.fndata.items() if "configs" in data
    ]
    exported = [conf for conf in utils.flatten(exported) if conf[1] == ctxtype]
    exported_names = [conf[0] for conf in exported]

    # if no setting is given, then list all settings for context.
    if not setting_str:
        await self.msg(
            modname, chan, ["settings: {}".format(", ".join(exported_names))]
        )
        return

    # is the setting we're trying to get/set a recognized, exported configuration value?
    if not setting_str in exported_names:
        await self.msg(modname, chan, [f"no such setting '{setting_str}'."])
        return

    setting = [s for s in exported if s[0] == setting_str][0]
    pattern = setting[2]
    description = setting[3]
    cast = setting[4]

    # if no value is given, print out the current value for the setting.
    if not value:
        cur_value = configuration.get(
            self.network, ctxname, setting_str, default="", cast=cast
        )
        await self.msg(
            modname, chan, [f"value of '{setting_str}' for {ctxname}: '{cur_value}'"]
        )
        return

    # don't let users change settings for channels they don't have +o in.
    # don't let users change settings for other users (unles they're bot admins)
    is_admin = await self.is_admin(nick)
    is_oper = _is_oper(self, ctxname, nick)
    if ctxtype == ConfigScope.CHAN and not is_oper and not is_admin:
        await self.msg(modname, chan, [f"you must have +o in {ctxname}"])
        return
    if (
        ctxtype == ConfigScope.USER
        and not ctxname == nick
        and not ctxname == user
        and not is_admin
    ):
        await self.msg(modname, chan, [f"permission denied"])
        return

    # ensure the value given is valid.
    if pattern and not re.match(pattern, value):
        if description:
            await self.msg(modname, chan, [f"invalid format (need: {description})"])
        else:
            await self.msg(modname, chan, [f"invalid format."])
        return

    try:
        configuration.try_cast(cast, value)
    except:
        if description:
            await self.msg(modname, chan, [f"invalid format (need: {description})"])
        else:
            await self.msg(modname, chan, [f"invalid format."])
        return

    # now we can set the value
    # NOTE: user pings are allowed intentionally
    configuration.set(self.network, ctxname, setting[0], value)
    await self.msg(modname, chan, [f"set '{setting[0]}' for '{ctxname}' to '{value}'"])


async def init(self):
    manager.register(self, bot_config_set)
