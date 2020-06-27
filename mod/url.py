# url-based functions
# TODO: get title of url
# TODO: unshorten url

import common, nullptr
modname = common.modname('url')

async def shorten(self, chan, msg, target = 'https://0x0.st/'):
    if len(msg) < 1:
        await self.message(chan, f'{modname} error: need url')

    try:
        res = nullptr.shorten(msg, nullptr = target)
    except:
        await self.message(chan, f'{modname} error: bad url')

    await self.message(chan, f'{modname} {res}')

async def shorten_0x0(self, chan, src, msg):
    await shorten(self, chan, msg)

async def shorten_ttm(self, chan, src, msg):
    await shorten(self, chan, msg, target = 'https://ttm.sh')

async def init(self):
    self.cmd['0x0'] = shorten_0x0
    self.cmd['ttm'] = shorten_ttm

    self.help['0x0'] = ['shorten <url> - shorten a url with 0x0.st']
    self.help['ttm'] = ['shorten <url> - shorten a url with ttm.sh']
