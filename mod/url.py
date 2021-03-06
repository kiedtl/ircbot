# url-based functions

import re
import urllib

import configuration
import manager
import nullptr
import gemini
import common

from manager import *
from bs4 import BeautifulSoup as BS

IS_URL = r"(https?|gemini)://\S+"
modname = "url"

class UnknownSchemeException(Exception):
    pass

def _url_scheme(url):
    return urllib.parse.urlparse(url).scheme

def _url_title(url, scheme):
    # TODO: gopher, finger
    if scheme.startswith("http"):
        http = urllib.request.urlopen(url)
        return BS(http).title.string
    elif scheme == "gemini":
        data = gemini.query(url)
        gemi = gemini.parse(data)
        return gemini.title(gemi)
    else:
        raise UnknownSchemeException()


@manager.hook(modname, "filterurl", hook=HookType.PATTERN, pattern=IS_URL)
@manager.config("http-titles",   ConfigScope.CHAN, desc="True or False", cast=bool)
@manager.config("gemini-titles", ConfigScope.CHAN, desc="True or False", cast=bool)
async def url_filter(self, chan, src, msg):
    try:
        scheme = _url_scheme(msg)
        if scheme.startswith("http"):
            if not configuration.get(self.network, chan, "http-titles", cast=bool):
                return
        elif scheme == "gemini":
            if not configuration.get(self.network, chan, "gemini-titles", cast=bool):
                return

        title = _url_title(msg, scheme)
        await self.msg(modname, chan, [title])
    except:
        return


async def title(self, chan, src, msg):
    if len(msg.strip()) > 0:
        txt = msg
    else:
        try:
            txt = common.get_backlog_msg(self, chan, msg)[1]
        except:
            await self.msg(modname, chan, ["no url found"])
            return

    # assume urls are HTTP if no scheme
    if not "://" in txt:
        txt = "http://" + txt

    try:
        title = _url_title(txt, _url_scheme(txt))
        await self.msg(modname, chan, [title])
    except UnknownSchemeException:
        await self.msg(modname, chan, [f"Invalid URL scheme."])
    except:
        await self.msg(modname, chan, [f"Invalid URL."])


async def _shorten(self, chan, msg, target="https://0x0.st/"):
    if len(msg) < 1:
        await self.msg(modname, chan, [f"need url"])
        return

    try:
        res = nullptr.shorten(msg, nullptr=target)
    except:
        await self.msg(modname, chan, [f"bad url"])
        return

    await self.msg(modname, chan, [f"{res}"])


async def shorten_0x0(self, chan, src, msg):
    await _shorten(self, chan, msg)


async def shorten_ttm(self, chan, src, msg):
    await _shorten(self, chan, msg, target="https://ttm.sh")


async def unshorten(self, chan, src, msg):
    if len(msg) < 1:
        await self.msg(modname, chan, [f"need url"])
        return

    try:
        res = nullptr.unshorten(msg)
    except:
        await self.msg(modname, chan, [f"bad url"])
        return

    await self.msg(modname, chan, [f"{res}"])


async def init(self):
    manager.register(self, url_filter)

    self.handle_cmd["0x0"] = shorten_0x0
    self.handle_cmd["ttm"] = shorten_ttm
    self.handle_cmd["title"] = title
    self.handle_cmd["unshorten"] = unshorten

    self.help["0x0"] = ["shorten [url] - shorten a url with 0x0.st"]
    self.help["ttm"] = ["shorten [url] - shorten a url with ttm.sh"]
    self.help["unshorten"] = ["unshorten [url] - try to unshorten a url"]
