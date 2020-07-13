# random commands that involve
# simply piping text into a command
# and posting the result

import nullptr, out, requests
modname = 'pape'

async def random_pape(self, chan, src, msg):
    # get random wallpaper
    rwal_url = 'https://source.unsplash.com/random/2400x1600'
    res = requests.get(url=rwal_url, allow_redirects=False)

    if res.status_code != 302:
        await out.msg(self, modname, chan, [f'could not get wallpaper'])
        return

    rwal = res.headers['Location']

    # the url is really long, so shorten
    # it first...
    try:
        shortened = nullptr.shorten(rwal)
    except:
        await out.msg(self, modname, chan, [f'could not shorten url'])
        return

    await out.msg(self, modname, chan, [f'{shortened}'])

async def search_pape(self, chan, src, msg):
    if len(msg) < 1:
        await out.msg(self, modname, chan, [f'need search terms'])
        return

    # get wallpaper
    query = msg.replace(' ', ',')
    search_url = f'https://source.unsplash.com/2400x1600/?{query}'
    res = requests.get(url=search_url, allow_redirects=False)

    if res.status_code != 302:
        await out.msg(self, modname, chan, [f'could not get wallpaper'])
        return

    wal = res.headers['Location']

    # the url is really long, so shorten
    # it first...
    try:
        shortened = nullptr.shorten(wal)
    except:
        await out.msg(self, modname, chan, [f'could not shorten url'])
        return

    await out.msg(self, modname, chan, [f'{shortened}'])

async def init(self):
    self.handle_cmd['rpape'] = random_pape
    self.handle_cmd['spape'] = search_pape

    self.help['rpape'] = ['rpape - get a random wallpaper from unsplash']
    self.help['spape'] = ['spape [query] - search for a wallpaper on unsplash']
