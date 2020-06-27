# url-based functions
# TODO: get title of url
# TODO: unshorten url

import nullptr, out
modname = 'url'

async def shorten(self, chan, msg, target = 'https://0x0.st/'):
    if len(msg) < 1:
        await out.msg(self, modname, chan, [f'need url'])
        return

    try:
        res = nullptr.shorten(msg, nullptr = target)
    except:
        await out.msg(self, modname, chan, [f'bad url'])
        return

    await out.msg(self, modname, chan, [f'{res}'])

async def shorten_0x0(self, chan, src, msg):
    await shorten(self, chan, msg)

async def shorten_ttm(self, chan, src, msg):
    await shorten(self, chan, msg, target = 'https://ttm.sh')

async def unshorten(self, chan, src, msg):
    if len(msg) < 1:
        await out.msg(self, modname, chan, [f'need url'])
        return

    try:
        res = nullptr.unshorten(msg)
    except:
        await out.msg(self, modname, chan, [f'bad url'])
        return

    await out.msg(self, modname, chan, [f'{res}'])

async def init(self):
    self.cmd['0x0'] = shorten_0x0
    self.cmd['ttm'] = shorten_ttm
    self.cmd['unshorten'] = unshorten

    self.help['0x0'] = ['shorten [url] - shorten a url with 0x0.st']
    self.help['ttm'] = ['shorten [url] - shorten a url with ttm.sh']
    self.help['unshorten'] = ['unshorten [url] - try to unshorten a url']
