# reddit stuff

import handlers
import fmt
import out
import reddit

modname = 'reddit'

PUSHSHIFT = 'https://api.pushshift.io/reddit/search/submission'

async def submissions_for_url(self, chan, src, msg):
    '''
    :name: rdu
    :hook: cmd
    :help: search for submissions for url on reddit.
    :args: @url:str
    '''
    if len(msg) < 1:
        await out.msg(self, modname, chan, [f'need url'])
        return

    await out.msg(self, modname, chan, ['searching...'])

    posts = reddit.search_by_url(msg)
    if len(posts) == 0:
        await out.msg(self, modname, chan, ['no results found'])
        return

    results = []
    for result in posts:
        # no nsfw please
        if result['over_18']:
            continue

        formatted = reddit.fmt_post_info(result)
        results.append(formatted)

    await out.msg(self, modname, chan, results)

async def init(self):
    handlers.register(self, modname, submissions_for_url)
