# reddit stuff
# TODO: STOP USING PUSHOVER and
# USE REDDIT'S API for HEAVEN's SAKE

import handlers
import fmt
import out
import re
import reddit

modname = 'reddit'

EXTRACTID = re.compile('(?:https?://)?(?:www\.|old\.|new\.)?(?:reddit.com/r/[a-zA-Z0-9]+/comments/([a-zA-Z0-9]+)/.*)|(?:redd.it/([a-zA-Z0-9]+))')

# TODO: auto show info for rd url
# TODO: search only in subreddit

async def submissions_search(self, chan, src, msg, args, opts):
    '''
    :name: rds
    :hook: cmd
    :help: search for posts on reddit.
    :args: &s:subreddit:str @keywords:list
    '''
    await out.msg(self, modname, chan, ['searching...'])

    if 's' in opts:
        sub = opts['s']
        if sub.startswith('r/'):
            sub = sub[2:]
        posts = reddit.search_by_keywords(msg, subreddit=sub)
    else:
        posts = reddit.search_by_keywords(msg)

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

async def submissions_for_url(self, chan, src, msg, args, opts):
    '''
    :name: rdu
    :hook: cmd
    :help: search for posts for url on reddit.
    :args: @url:str
    '''
    # TODO: check backlog too
    # TODO: ensure that url is valid
    if len(msg) < 1:
        await out.msg(self, modname, chan, [f'need url'])
        return

    await out.msg(self, modname, chan, ['searching...'])

    if 's' in opts:
        sub = opts['s']
        if sub.startswith('r/'):
            sub = sub[2:]
        posts = reddit.search_by_url(msg, subreddit=sub)
    else:
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

async def submission_info(self, chan, src, msg, args, opts):
    '''
    :name: rdi
    :hook: cmd
    :help: show info for reddit url
    :args: @url:str
    '''
    # TODO: check backlog too
    # TODO: ensure that url is valid
    if len(msg) < 1:
        await out.msg(self, modname, chan, [f'need url'])
        return

    results = EXTRACTID.findall(msg)[0]
    rd_id = results[0] or results[1]

    if rd_id == '':
        await out.msg(self, modname, chan, [f'bad url'])
        return

    await out.msg(self, modname, chan, ['searching...'])

    posts = reddit.search_by_id(rd_id)
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
    handlers.register(self, modname, submissions_search)
    handlers.register(self, modname, submissions_for_url)
    handlers.register(self, modname, submission_info)
