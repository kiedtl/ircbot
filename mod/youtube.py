# youtube utility functions

import youtube as YT
import common, re, botsecrets
import handlers

modname = "youtube"
is_yturl = re.compile(
    "(?:.*)?(https?\://(?:www\.|m\.)?(?:youtu.be/|youtube.com/)(?:[^ ]+)?)"
)
youtube = YT.authenticate(botsecrets.yt_key)


async def handle_yt(self, chan, src, msg):
    """
    :name: handle_yt
    :hook: reg
    :hook_regex: (?:.*)?(https?\://(?:www\.|m\.)?(?:youtu.be/|youtube.com/)(?:[^ ]+)?)
    """
    """
    Detect a YT url in chat.
    """
    matches = is_yturl.findall(msg)
    if len(matches) < 1:
        return
    try:
        v_id = YT.id_from_url(matches[0])
    except:
        return

    info = YT.video_info(youtube, v_id)
    info_fmted = YT.fmt_video_info(info)
    await self.msg(modname, chan, [info_fmted])


async def yt_info(self, chan, src, msg):
    """
    :name: youtube
    :hook: cmd
    :help: show info for a youtube url [num] messages back
    :args: @num:int
    :aliases: yt
    """
    try:
        txt = common.get_backlog_msg(self, chan, msg)[1]
    except:
        await self.msg(modname, chan, ["no youtube url found"])
        return

    matches = is_yturl.findall(txt)
    if len(matches) < 1:
        await self.msg(modname, chan, [f"no url in {txt}"])
        return
    try:
        v_id = YT.id_from_url(matches[0])
    except:
        await self.msg(modname, chan, [f"bad url"])
        return

    info = YT.video_info(youtube, v_id)
    info_fmted = YT.fmt_video_info(info)
    await self.msg(modname, chan, [info_fmted])


async def init(self):
    # disabled, now that tildebot is a thing
    # handlers.register(self, modname, handle_yt)
    handlers.register(self, modname, yt_info)
