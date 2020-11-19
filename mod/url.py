# url-based functions

# REQUIRE lib bs4
# REQUIRE lib urllib

import common, re, urllib, nullptr
from bs4 import BeautifulSoup as BS

modname = "url"


async def handle_url(self, chan, src, msg):
    """
    Detect a url in chat.
    """
    try:
        http = urllib.request.urlopen(msg)
        data = BS(http)
    except:
        return
    await self.msg(modname, chan, [data.title.string])


async def title(self, chan, src, msg):
    try:
        txt = common.get_backlog_msg(self, chan, msg)[1]
    except:
        await self.msg(modname, chan, [self.err_backlog_too_short])
        return

    if not txt.startswith("http"):
        txt = "http://" + txt

    try:
        http = urllib.request.urlopen(txt)
        data = BS(http)
    except:
        await self.msg(modname, chan, [f"bad url"])
        return
    await self.msg(modname, chan, [data.title.string])


async def shorten(self, chan, msg, target="https://0x0.st/"):
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
    await shorten(self, chan, msg)


async def shorten_ttm(self, chan, src, msg):
    await shorten(self, chan, msg, target="https://ttm.sh")


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
    url_re = re.compile(r"https?://\S+", re.I)

    # disabled, now that tildebot is a thing
    # self.handle_reg['url'] = (url_re, handle_url)

    self.handle_cmd["0x0"] = shorten_0x0
    self.handle_cmd["ttm"] = shorten_ttm
    self.handle_cmd["title"] = title
    self.handle_cmd["unshorten"] = unshorten

    self.help["0x0"] = ["shorten [url] - shorten a url with 0x0.st"]
    self.help["ttm"] = ["shorten [url] - shorten a url with ttm.sh"]
    self.help["unshorten"] = ["unshorten [url] - try to unshorten a url"]
