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

IS_URL = r"(?:.*)?((?:https?|gemini)://\S+)"
modname = "url"


class UnknownScheme(Exception):
    pass
class InvalidContentType(Exception):
    pass


def _url_scheme(url):
    return urllib.parse.urlparse(url).scheme


def _url_title(url, scheme):
    # TODO: gopher, finger
    if scheme.startswith("http"):
        http = urllib.request.urlopen(url)
        type = http.getheader('content-type')
        if type and type is not 'text/html':
            raise InvalidContentType()
        return BS(http).title.string
    elif scheme == "gemini":
        data = gemini.query(url)
        gemi = gemini.parse(data)
        return gemini.title(gemi)
    else:
        raise UnknownScheme()


@manager.hook(modname, "filterurl", hook=HookType.PATTERN, pattern=IS_URL)
@manager.config("http-titles", ConfigScope.CHAN, desc="True or False", cast=bool)
@manager.config("gemini-titles", ConfigScope.CHAN, desc="True or False", cast=bool)
async def url_filter(self, chan, src, msg):
    url_matches = re.findall(IS_URL, msg)
    if len(url_matches) < 1:
        return

    try:
        scheme = _url_scheme(url_matches[0])
        if scheme.startswith("http"):
            if not configuration.get(self.network, chan, "http-titles", cast=bool):
                return
        elif scheme == "gemini":
            if not configuration.get(self.network, chan, "gemini-titles", cast=bool):
                return

        title = _url_title(url_matches[0], scheme)
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
    except UnknownScheme:
        await self.msg(modname, chan, [f"Invalid URL scheme."])
    except InvalidContentType:
        await self.msg(modname, chan, [f"Not an HTML document."])
    except urllib.error.HTTPError as e:
        await self.msg(modname, chan, [f"{e}"])
    except Exception as e:
        await self.msg(modname, chan, [f"Failed to get title.", f"{e}"])


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
