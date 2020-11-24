import dataclasses
import re
import utils

from functools import partial
from dataclasses import field
from typing import List, Tuple


ArgType = utils.enum(INT=0, STR=1, LIST=2)


@dataclasses.dataclass
class Arg:
    name: str
    desc: str = ""
    argtype: ArgType = ArgType.STR
    optional: bool = False


ConfigScope = utils.enum(USER=0, CHAN=1)
HookType = utils.enum(COMMAND="cmd", RAW="raw", PATTERN="reg")
AccessType = utils.enum(ANY=0, IDENTIFIED=1, ADMIN=2, CHAN_OP=3, CHAN_HOP=4, CHAN_VOP=5)

FNINFO_ATTR = "fninfo"


@dataclasses.dataclass
class FunctionInfo:
    name: str = ""
    hook_type: HookType = HookType.COMMAND
    args: List[Arg] = field(default_factory=lambda: [])
    module: str = ""

    # only used when hook_type == HookType.PATTERN
    pattern: re.Pattern = None

    # only used when hook_type == HookType.COMMAND
    helptext: List[str] = field(default_factory=lambda: [])
    access: AccessType = AccessType.ANY
    aliases: List[str] = field(default_factory=lambda: [])

    # "exported" configuration values.
    # tuple structure: <name>, <scope>, <pattern>, <desc>, <cast>
    # <pattern> is the valid format in regex form, <desc> is the same as <pattern>
    # but in human-readable format.
    configs: List[Tuple[str, ConfigScope, str, str, type]] = field(
        default_factory=lambda: []
    )


def _fn_get_info(fn):
    if not hasattr(fn, FNINFO_ATTR):
        setattr(fn, FNINFO_ATTR, FunctionInfo())
    return getattr(fn, FNINFO_ATTR)


def hook(
    module, name, aliases=[], access=AccessType.ANY, hook=HookType.COMMAND, pattern=None
):
    def decorator(func):
        fninfo = _fn_get_info(func)
        fninfo.module = module
        fninfo.name = name
        fninfo.access = access
        fninfo.hook_type = hook
        fninfo.aliases = aliases

        if hook == HookType.PATTERN:
            fninfo.pattern = re.compile(pattern)

        setattr(func, FNINFO_ATTR, fninfo)
        return func

    return decorator


# deprecated.
def argument(name, desc=None, argtype=ArgType.STR, optional=False):
    def decorator(func):
        arg = Arg(name=name, desc=desc, argtype=argtype, optional=optional)
        fninfo = _fn_get_info(func)
        fninfo.args.append(arg)
        setattr(func, FNINFO_ATTR, fninfo)
        return func

    return decorator


def arguments(args):
    def decorator(func):
        fninfo = _fn_get_info(func)
        fninfo.args = args
        setattr(func, FNINFO_ATTR, fninfo)
        return func

    return decorator


# deprecated.
def aliases(aliases):
    def decorator(func):
        fninfo = _fn_get_info(func)
        fninfo.aliases = aliases
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


def config(conf, ctx, pattern=None, desc=None, cast=None):
    """
    'Export' a configuration value, making
    it possible for users/opers to edit them.
    """

    def decorator(func):
        fninfo = _fn_get_info(func)
        fninfo.configs.append((conf, ctx, pattern, desc, cast))
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
            if arg.desc:
                help_string += arg.desc + " "
            else:
                if arg.optional:
                    help_string += f"[{arg.name}] "
                else:
                    help_string += f"<{arg.name}> "

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
        "configs": fninfo.configs,
        "module": fninfo.module,
        "func": func,
    }

    if fninfo.access == AccessType.ADMIN:
        data["require_admin"] = True
    elif fninfo.access == AccessType.CHAN_OP:
        data["require_op"] = True
    elif fninfo.access == AccessType.CHAN_HOP:
        data["require_hop"] = True
    elif fninfo.access == AccessType.CHAN_VOP:
        data["require_vop"] = True
    elif fninfo.access == AccessType.IDENTIFIED:
        data["require_identified"] = True

    data["args"] = []
    for arg in fninfo.args:
        data_arg = {}
        data_arg["name"] = arg.name
        data_arg["desc"] = arg.desc

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
