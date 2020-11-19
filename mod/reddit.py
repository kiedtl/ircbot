# reddit stuff

import handlers
import fmt
import re
import reddit

modname = "reddit"

EXTRACTID = re.compile(
    "(?:https?://)?(?:www\.|old\.|new\.)?(?:reddit.com/r/[a-zA-Z0-9]+/comments/([a-zA-Z0-9]+)/.*)|(?:redd.it/([a-zA-Z0-9]+))"
)

# TODO: auto show info for rd url
# TODO: search only in subreddit


async def submissions_search(self, chan, src, msg, args, opts):
    """
    :name: redditsearch
    :hook: cmd
    :help: search for posts on reddit.
    :args: &s:subreddit:str keywords:list
    :aliases: rds
    """
    await self.msg(modname, chan, ["searching..."])

    if "s" in opts:
        sub = opts["s"]
        if sub.startswith("r/"):
            sub = sub[2:]
        posts = reddit.search_by_keywords(msg, subreddit=sub)
    else:
        posts = reddit.search_by_keywords(msg)

    if len(posts) == 0:
        await self.msg(modname, chan, ["no results found"])
        return

    results = []
    for result in posts:
        # no nsfw please
        if result["over_18"]:
            continue

        formatted = reddit.fmt_post_info(result)
        results.append(formatted)

    await self.msg(modname, chan, results)


async def submissions_for_url(self, chan, src, msg, args, opts):
    """
    :name: redditurl
    :hook: cmd
    :help: search for posts for url on reddit.
    :args: &s:subreddit:str @url:str
    :aliases: rdu
    """
    # TODO: check backlog too
    # TODO: ensure that url is valid
    if len(msg) < 1:
        await self.msg(modname, chan, [f"need url"])
        return

    await self.msg(modname, chan, ["searching..."])

    if "s" in opts:
        sub = opts["s"]
        if sub.startswith("r/"):
            sub = sub[2:]
        posts = reddit.search_by_url(msg, subreddit=sub)
    else:
        posts = reddit.search_by_url(msg)

    if len(posts) == 0:
        await self.msg(modname, chan, ["no results found"])
        return

    results = []
    for result in posts:
        # no nsfw please
        if result["over_18"]:
            continue

        formatted = reddit.fmt_post_info(result)
        results.append(formatted)

    await self.msg(modname, chan, results)


async def submission_info(self, chan, src, msg, args, opts):
    """
    :name: redditinfo
    :hook: cmd
    :help: show info for reddit url
    :args: @url:str
    :aliases: rdi
    """
    # TODO: check backlog too
    # TODO: ensure that url is valid
    if len(msg) < 1:
        await self.msg(modname, chan, [f"need url"])
        return

    results = EXTRACTID.findall(msg)[0]
    rd_id = results[0] or results[1]

    if rd_id == "":
        await self.msg(modname, chan, [f"bad url"])
        return

    await self.msg(modname, chan, ["searching..."])

    posts = reddit.search_by_id(rd_id)
    if len(posts) == 0:
        await self.msg(modname, chan, ["no results found"])
        return

    results = []
    for result in posts:
        # no nsfw please
        if result["over_18"]:
            continue

        formatted = reddit.fmt_post_info(result)
        results.append(formatted)

    await self.msg(modname, chan, results)


async def init(self):
    handlers.register(self, modname, submissions_search)
    handlers.register(self, modname, submissions_for_url)
    handlers.register(self, modname, submission_info)
