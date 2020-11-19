# youtube utility functions

import youtube as YT
import common, re, secrets

modname = "youtube"
is_yturl = re.compile(
    "(?:.*)?(https?\://(?:www\.|m\.)?(?:youtu.be/|youtube.com/)(?:[^ ]+)?)"
)
youtube = YT.authenticate(secrets.yt_key)


async def handle_yt(self, chan, src, msg):
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
    try:
        txt = common.get_backlog_msg(self, chan, msg)[1]
    except:
        await self.msg(modname, chan, [self.err_backlog_too_short])
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
    # self.handle_reg['youtube'] = (is_yturl, handle_yt)
    self.handle_cmd["youtube"] = yt_info

    self.aliases["youtube"] = ["yt"]

    self.help["youtube"] = [
        "yt [num] - show info for a youtube url [num] messages back"
    ]
