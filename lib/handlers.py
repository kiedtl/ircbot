# REQUIRE lib getopt

#
# helper functions to deal with
# handlers.
#

import getopt
from getopt import gnu_getopt
import out

# TODO: documentation on how this whole file,
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
    Ensure that all the necessary arguments
    are in place, parse non-positional arguments,
    and run function.
    """
    if func not in self.fndata:
        await func(self, chan, src, msg)
        return

    shortopts = ""

    # create list of short opts
    for arg in self.fndata[func]["args"]:
        if "option" in arg:
            shortopts += arg["option"]
            shortopts += ":"
        elif "flag" in arg:
            shortopts += arg["flag"]

    try:
        opts, args = gnu_getopt(msg.split(), shortopts)
    except getopt.GetoptError as err:
        await out.msg(self, self.fndata[func]["module"], chan, [f"{err}"])
        return

    # -------------------------------
    #     ***MESSY MESSY MESSY***
    # -------------------------------

    # ensure all non-optional arguments are in place
    non_optional = [
        a
        for a in self.fndata[func]["args"]
        if not a["optional"] and "option" not in a and "flag" not in a
    ]

    if len(args) < len(non_optional):
        # all the required arguments aren't there!
        name = non_optional[len(args)]["name"]
        await out.msg(
            self, self.fndata[func]["module"], chan, [f"need argument {name}"]
        )
        return

    await func(self, chan, src, msg, args, dict(opts))


def register(self, modname, func):
    """
    Parse a functions docstring and then
    register it as a {cmd, raw, regex} handler.
    Set helptext and aliases, too.
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
        return

    last_item = ""

    for line in doc.split("\n"):
        line = line.lstrip(" ")
        if len(line) < 1:
            continue
        elif line[0] == ":":
            key, _, value = line.partition(": ")
            key = key.lstrip(":")
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

        # is it a flag?
        # flags follow this syntax when defined
        # in a function docstring:
        #   [&/*]<shortopt_char>:<opt_name>:<type>
        # if the prefix is '&', it takes an argument,
        # if the prefix is '*', if doesn't take args.
        if raw_arg[0] == "&":
            arg["option"] = raw_arg[1]
            raw_arg = raw_arg[3:]
        elif raw_arg[0] == "*":
            arg["flag"] = raw_arg[1]
            raw_arg = raw_arg[3:]

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
            elif "flag" in arg:
                help_string += f'[-{arg["flag"]} ({arg["name"]})] '
            elif "option" in arg:
                help_string += f'[-{arg["option"]} {arg["name"]}] '
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
