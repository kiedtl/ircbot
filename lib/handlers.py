# REQUIRE lib getopt

#
# helper functions to deal with
# handlers.
#

import config
import re
import utils

Msg = utils.enum(RAW=0, OK=1, ERR=2)

# TODO: documentation on how this whole file
# works, so when I inevitably leave this project
# to rot for a month I won't come back completely
# confused.
#
# FIXME: so, when we check to make sure that
# all the required arguments to a command are there,
# we use the *very* naive method of checking
# that the number of arguments is greater than
# the amount of required arguments.
#
# however... some arguments actually take
# *more than one* value, which makes this dumb
# method fall to pieces.
#
# example: the keywords arguments of :rds
# (see mod/reddit.py). it's type is "list",
# which means that it takes a list of strings as
# its argument.


async def execute(self, func, chan, src, msg):
    """
    Ensure that all the necessary arguments are in place,
    and run the function.
    """

    async def error(text):
        await self.msg(self.fndata[func]["module"], chan, [text])

    if func not in self.fndata:
        await func(self, chan, src, msg)
        return

    if "require_identified" in self.fndata[func]:
        if self.users[src]["account"] == None:
            await error("you must identify with NickServ to use this command.")
            return
    if "require_admin" in self.fndata[func]:
        if not await self.is_admin(src):
            await error("permission denied (admin-only command).")
            return
    if "require_op" in self.fndata[func]:
        # operator
        if not src in self.channels[chan]["modes"]["o"]:
            await error(f"you must be an operator in this channel.")
            return
    if "require_hop" in self.fndata[func]:
        # half operator
        if not src in self.channels[chan]["modes"]["h"]:
            await error(f"you must be an half-operator in this channel.")
            return
    if "require_vop" in self.fndata[func]:
        # voice
        if not src in self.channels[chan]["modes"]["v"]:
            await error(f"you must have +v in this channel.")
            return

    # ensure all non-optional arguments are in place
    non_optional = [a for a in self.fndata[func]["args"] if not a["optional"]]

    if len(msg.split()) < len(non_optional):
        # all the required arguments aren't there!
        missing = non_optional[len(msg.split())]["name"]
        await error(
            f"not enough arguments (need argument '{missing}'). see '{config.prefix}help {self.fndata[func]['name']}'."
        )
        return

    ret = await func(self, chan, src, msg)

    # if the handler returns anything, print it to IRC.
    # the returned data should be a Tuple[Msg, List[str]]
    if ret and type(ret) == tuple:
        msgtype = ret[0]
        msgstr = ret[1]

        if type(msgstr) == str:
            msgstr = [msgstr]

        if msgtype == Msg.RAW:
            await self.message(chan, msgstr[0])
        elif msgtype == Msg.OK or msgtype == Msg.ERR:
            await self.msg(self.fndata[func]["module"], chan, msgstr)


def register(self, modname, func):
    """
    Parse a function's docstring and then register it
    as a {cmd, raw, regex} handler. Set helptext and aliases, too.
    """

    # TODO: cleanup data parsing
    # separate lexing from parsing
    #
    # TODO: split this up into multiple
    # functions

    # has this function already been registered?
    if hasattr(func, "registered"):
        return

    data = {}
    data["name"] = ""
    data["help"] = []
    data["args"] = ""
    data["func"] = func
    data["module"] = modname

    doc = func.__doc__ or False
    if not doc:
        self.log(
            "handlers",
            f"Tried to register function in module {modname} that had no docstring.",
        )
        return

    last_item = ""

    for line in doc.split("\n"):
        line = line.lstrip(" ")
        if len(line) < 1:
            continue
        elif line[0] == ":":
            key, _, value = line.partition(": ")
            key = key.lstrip(":").rstrip(":")
            if key in data and type(data[key]) is list:
                data[key].append(value)
            else:
                data[key] = value
            last_item = key
        elif line[0] == ">":
            if last_item == "":
                continue
            strpd = line.lstrip(">").lstrip(" ")
            if type(data[last_item]) is list:
                data[last_item][-1] += " " + strpd
            elif type(data[last_item]) is str:
                data[last_item] += strpd

    # parse arguments
    raw_args = data["args"]
    data["args"] = []
    for raw_arg in raw_args.split():
        arg = {}

        # optional?
        if raw_arg[0] == "@":
            arg["optional"] = True
            raw_arg = raw_arg.lstrip("@")
        else:
            arg["optional"] = False

        name, _, _type = raw_arg.partition(":")
        arg["name"] = name
        arg["type"] = _type

        data["args"].append(arg)

    # register aliases
    aliases = []
    if "aliases" in data:
        aliases = data["aliases"].split()
        self.aliases[data["name"]] = aliases

    # format help string with name and args
    if len(data["help"]) > 0:
        if "aliases" in data and len(aliases) > 0:
            help_string = data["name"] + "/" + "/".join(aliases) + " "
        else:
            help_string = data["name"] + " "

        for arg in data["args"]:
            if arg["optional"]:
                help_string += f'[{arg["name"]}] '
            else:
                help_string += f'<{arg["name"]}> '
        help_string += "- " + data["help"][0]

        # register help messages
        self.help[data["name"]] = [help_string] + data["help"][1:]

    # register handlers
    if "hook" in data:
        if data["hook"] == "cmd":
            self.handle_cmd[data["name"]] = func
        elif data["hook"] == "raw":
            self.handle_raw[data["name"]] = func
        elif data["hook"] == "reg":
            reg = re.compile(data["hook_regex"])
            self.handle_reg[data["name"]] = (reg, func)

    # register rest of data
    self.fndata[func] = data

    func.registered = True
    return
