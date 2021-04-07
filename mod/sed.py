import configuration
import fmt
import manager
import re

from manager import *
from handlers import *

modname = "text"

IS_SED = r"^(?:(?P<user>[a-zA-Z0-9_\-\\\[\]\{\}^`|]+): )?(?P<sed>s/[^/]+/[^/]*/)(?P<seds> s/[^/]+/[^/]*/)*"
IS_SED_comp = re.compile(IS_SED)
IS_SED_LIBERAL = re.compile(r"^(([a-zA-Z0-9_\-\\\[\]\{\}^`|]+): )?(s/[^/]+/[^/]*/?)")


def _sed(e, m):
    parsed = e.split("/")
    b = parsed[1]
    a = parsed[2]

    try:
        return re.sub(b, a, m)
    except:
        return m


@manager.hook(modname, "filtersed", hook=HookType.PATTERN, pattern=IS_SED)
@manager.config("sed-pattern", ConfigScope.CHAN, desc="True or False", cast=bool)
async def filtersed(self, chan, src, msg):
    enabled = configuration.get(self.network, chan, "sed-pattern", cast=bool)
    if not enabled:
        return

    sections = IS_SED_comp.match(msg).groupdict()
    user = sections["user"] or src

    sedinput = None
    if chan in self.backlog and len(self.backlog[chan]):
        backlog = list(reversed(self.backlog[chan]))
        for back_msg in backlog:
            if back_msg[0] == user:
                if IS_SED_LIBERAL.match(back_msg[1]):
                    continue
                if _sed(sections["sed"], back_msg[1]) is sedinput:
                    continue
                sedinput = back_msg[1]
                break

    if not sedinput:
        return

    sedded = _sed(sections["sed"], sedinput)
    user_noping = fmt.zwnj(user)
    await self.message(chan, f"<{user}> {sedded}")


async def init(self):
    manager.register(self, filtersed)
