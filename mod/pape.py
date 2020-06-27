# random commands that involve
# simply piping text into a command
# and posting the result

import common, nullptr, requests
modname = common.modname('pape')

async def random_pape(self, chan, src, msg):
    # get random wallpaper
    rwal_url = 'https://source.unsplash.com/random/2400x1600'
    res = requests.get(url=rwal_url, allow_redirects=False)

    if res.status_code != 302:
        await self.message(chan,
            f'{modname} error: could not get wallpaper')
        return

    rwal = res.headers['Location']

    # the url is really long, so shorten
    # it first...
    try:
        shortened = nullptr.shorten(rwal)
    except:
        await self.message(chan,
            f'{modname} error: could not shorten wallpaper link')
        return

    await self.message(chan, f'{modname} {shortened}')

async def init(self):
    self.cmd['rpape'] = random_pape

    self.help['rpape'] = ['rpape - get a random wallpaper from unsplash']
