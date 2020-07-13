# url-based functions

import common, re, urllib, nullptr, irc
from bs4 import BeautifulSoup as BS
modname = 'url'

async def filterurl(self, chan, src, msg):
    """
    Detect a url in chat.
    """
    if self.url_re.match(msg):
        try:
            http = urllib.request.urlopen(msg)
            data = BS(http)
        except:
            return
        await irc.msg(modname, chan, [data.title.string])

async def title(self, chan, src, msg):
    try:
        txt = common.get_backlog_msg(self, chan, msg)[1]
    except:
        await irc.msg(modname, chan,
            [self.err_backlog_too_short])
        return

    if not txt.startswith('http'):
        txt = 'http://' + txt

    try:
        http = urllib.request.urlopen(txt)
        data = BS(http)
    except:
        await irc.msg(modname, chan,
            [f'bad url'])
        return
    await irc.msg(modname, chan, [data.title.string])

async def shorten(self, chan, msg, target = 'https://0x0.st/'):
    if len(msg) < 1:
        await irc.msg(modname, chan, [f'need url'])
        return

    try:
        res = nullptr.shorten(msg, nullptr = target)
    except:
        await irc.msg(modname, chan, [f'bad url'])
        return

    await irc.msg(modname, chan, [f'{res}'])

async def shorten_0x0(self, chan, src, msg):
    await shorten(self, chan, msg)

async def shorten_ttm(self, chan, src, msg):
    await shorten(self, chan, msg, target = 'https://ttm.sh')

async def unshorten(self, chan, src, msg):
    if len(msg) < 1:
        await irc.msg(modname, chan, [f'need url'])
        return

    try:
        res = nullptr.unshorten(msg)
    except:
        await irc.msg(modname, chan, [f'bad url'])
        return

    await irc.msg(modname, chan, [f'{res}'])

async def init(self):
    # disabled, now that tildebot is a thing
    #self.handle_raw['url'] = filterurl

    self.cmd['0x0'] = shorten_0x0
    self.cmd['ttm'] = shorten_ttm
    self.cmd['title'] = title
    self.cmd['unshorten'] = unshorten

    self.help['0x0'] = ['shorten [url] - shorten a url with 0x0.st']
    self.help['ttm'] = ['shorten [url] - shorten a url with ttm.sh']
    self.help['unshorten'] = ['unshorten [url] - try to unshorten a url']

    self.url_re = re.compile(r'https?://\S+', re.I)
