# youtube garbage stuff -_-

import youtube as YT
import common, out, re, secrets

modname = 'youtube'
is_yturl = re.compile(r'https?://(www\.|m\.)?(youtu.be/|youtube.com/)')
youtube = YT.authenticate(secrets.yt_key)

async def filteryt(self, chan, src, msg):
    """
    Detect a YT url in chat.
    """
    if not is_yturl.match(msg):
        return
    try:
        v_id = YT.id_from_url(msg)
    except:
        return

    info = YT.video_info(youtube, v_id)
    info_fmted = YT.fmt_video_info(info)
    await out.msg(self, modname, chan, [info_fmted])

async def yt_info(self, chan, src, msg):
    try:
        txt = common.get_backlog_msg(self, chan, msg)[1]
    except:
        await out.msg(self, modname, chan,
            [self.err_backlog_too_short])
        return

    try:
        v_id = YT.id_from_url(txt)
    except:
        await out.msg(self, modname, chan, [f'bad url'])
        return

    info = YT.video_info(youtube, v_id)
    info_fmted = YT.fmt_video_info(info)
    await out.msg(self, modname, chan, [info_fmted])

async def init(self):
    # disabled, now that tildebot is a thing
    self.handle_raw['yturl'] = filteryt

    self.cmd['youtube'] = yt_info
    self.cmd['yt'] = yt_info

    self.help['yt'] = ['yt [num] - display info for a youtube url [num] messages back']
