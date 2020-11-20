# NOTE: command-line-style flags are not supported, as I feel I made
# a mistake when I added them earlier. IRC bots are not command-line
# programs and should not act like they are.

import dataclasses
import re

from functools import partial
from dataclasses import field
from typing import List

def _enum(**items):
    return type('Enum', (), items)

ArgType = _enum(INT=0, STR=1, LIST=2)

@dataclasses.dataclass
class FunctionArg:
    name: str
    description: str
    argtype: ArgType
    optional: bool

HookType = _enum(COMMAND='cmd', RAW='raw', PATTERN='reg')
AccessType = _enum(ANY=0, ADMIN=1, CHAN_OP=2, CHAN_HOP=3, CHAN_VOP=4)

FNINFO_ATTR = "fninfo"

@dataclasses.dataclass
class FunctionInfo:
    name: str = ""
    hook_type: HookType = HookType.COMMAND
    args: List[FunctionArg] = field(default_factory=lambda: [])
    module: str = ""

    # only used when hook_type == HookType.PATTERN
    pattern: re.Pattern = None

    # only used when hook_type == HookType.COMMAND
    helptext: List[str] = field(default_factory=lambda: [])
    access: AccessType = AccessType.ADMIN
    aliases: List[str] = field(default_factory=lambda: [])


def _fn_get_info(fn):
    if not hasattr(fn, FNINFO_ATTR):
        setattr(fn, FNINFO_ATTR, FunctionInfo())
    return getattr(fn, FNINFO_ATTR)


def hook(module, name, hook=HookType.COMMAND, pattern=None):
    def decorator(func):
        fninfo = _fn_get_info(func)
        fninfo.module = module
        fninfo.name = name
        fninfo.hook_type = hook

        if hook == HookType.PATTERN:
            fninfo.pattern = re.compile(pattern)

        setattr(func, FNINFO_ATTR, fninfo)
        return func
    return decorator


def argument(name, desc="", argtype=ArgType.STR, optional=False):
    def decorator(func):
        arg = FunctionArg(name=name, description=desc,
                argtype=argtype, optional=optional)
        fninfo = _fn_get_info(func)
        fninfo.args.append(arg)
        setattr(func, FNINFO_ATTR, fninfo)
        return func
    return decorator


def access(access):
    def decorator(func):
        fninfo = _fn_get_info(func)
        fninfo.access = access
        setattr(func, FNINFO_ATTR, fninfo)
        return func
    return decorator


def alias(alias):
    def decorator(func):
        fninfo = _fn_get_info(func)
        fninfo.alias.append(alias)
        setattr(func, FNINFO_ATTR, fninfo)
        return func
    return decorator


def helptext(helptexts):
    def decorator(func):
        fninfo = _fn_get_info(func)
        for helptext in helptexts:
            fninfo.helptext.append(helptext)
        setattr(func, FNINFO_ATTR, fninfo)
        return func
    return decorator


def register(self, func):
    if hasattr(func, "registered"):
        return

    fninfo = _fn_get_info(func)

    # register aliases
    self.aliases[fninfo.name] = fninfo.aliases

    # format helptext with name of command, args, aliases, etc
    if len(fninfo.helptext) > 0:
        help_string = ""

        if len(fninfo.aliases) > 0:
            help_string = fninfo.name + "/" + "/".join(fninfo.aliases) + " "
        else:
            help_string = fninfo.name + " "

        for arg in fninfo.args:
            if arg.optional:
                help_string += f'[{arg.name}] '
            else:
                help_string += f'>{arg.name}> '

        help_string += "── " + fninfo.helptext[0]

        # register help message
        self.help[fninfo.name] = [help_string] + fninfo.helptext[1:]

    # register handlers
    if fninfo.hook_type == HookType.COMMAND:
        self.handle_cmd[fninfo.name] = func
    elif fninfo.hook_type == HookType.PATTERN:
        self.handle_reg[fninfo.name] = (fninfo.pattern, func)
    elif fninfo.hook_type == HookType.RAW:
        self.handle_raw[fninfo.name] = func

    # register rest of data
    data = {
        "name": fninfo.name,
        "help": fninfo.helptext,
        "func": func,
        "module": fninfo.module,
    }

    if fninfo.access == AccessType.ADMIN:
        data["require_admin"] = True
    elif fninfo.access == AccessType.CHAN_OP:
        data["require_op"] = True
    elif fninfo.access == AccessType.CHAN_HOP:
        data["require_hop"] = True
    elif fninfo.access == AccessType.CHAN_VOP:
        data["require_vop"] = True

    data["args"] = []
    for arg in fninfo.args:
        data_arg = {}
        data_arg["name"] = arg.name

        if arg.optional:
            data_arg["optional"] = True
        else:
            data_arg["optional"] = False

        if arg.argtype == ArgType.INT:
            data_arg["type"] = "int"
        elif arg.argtype == ArgType.LIST:
            data_arg["type"] = "list"
        elif arg.argtype == ArgType.STR:
            data_arg["type"] = "str"

        data["args"].append(data_arg)

    self.fndata[func] = data
    func.registered = True
