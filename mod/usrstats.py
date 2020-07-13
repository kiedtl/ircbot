import out
from common import nohighlight
modname = 'user stats'

# TODO: move to common
def get_all_logs(chan, msg):
    logf = open('irc/{}.log'.format(chan))
    rawlogs = logf.read().split('\n')
    logf.close()

    logs = []
    for line in rawlogs:
        data = line.split(' ', 3)
        if len(data) < 3:
            continue
        time = data[0]
        user = data[1]
        mesg = data[2]
        logs.append(
            {
                'time': time,
                'user': user,
                'msg':  mesg
            }
        )
    return logs

async def get_stats_by_phrase(self, chan, src, msg, phrases, label):
    stats = {}
    total = 0
    logs = []
    targetchan = chan
    if len(msg) > 0 and msg[:1] == '#':
        targetchan = msg

    try:
        logs = get_all_logs(targetchan, msg)
    except:
        await out.msg(self, modname, chan, [self.err_invalid_logfile])
        return

    for item in logs:
        if any(phrase in item['msg'] for phrase in phrases):
            if not item['user'] in stats:
                stats[item['user']] = 0
            stats[item['user']] += 1

    output = ''
    ctr = 0
    until = 7
    for i in sorted(stats.items(), key=lambda i: i[1], reverse=True):
        if ctr == until:
            break
        output += ('{} ({} msgs), '
            .format(nohighlight(i[0]), i[1]))
        ctr += 1
    output = output[:-2] # trim ', '
    await out.msg(self, modname, chan,
        [f'{label} people at {targetchan}: {output}'])

async def noisiest(self, chan, src, msg):
    stats = {}
    total = 0
    logs = []
    targetchan = chan
    if len(msg) > 0 and msg[:1] == '#':
        targetchan = msg

    try:
        logs = get_all_logs(targetchan, msg)
    except:
        await out.msg(self, modname, chan, [self.err_invalid_logfile])
        return

    for item in logs:
        if not item['user'] in stats:
            stats[item['user']] = 0
        stats[item['user']] += 1
        total += 1

    output = ''
    ctr = 0
    until = 7
    for i in sorted(stats.items(), key=lambda i: i[1], reverse=True):
        if ctr == until:
            break
        percentage = '{0:.2f}'.format(i[1] * 100 / total)
        output += ('{} ({}%, {} msgs), '
            .format(nohighlight(i[0]), percentage, i[1]))
        ctr += 1
    output = output[:-2] # trim ', '
    await out.msg(self, modname, chan,
        [f'top talkers at {targetchan}: {output}'])

async def happiest(self, chan, src, msg):
    happy = ['lol', 'lmao', ':)', ':-)', ':^)', ':D' ':-D', ';)', 'c:']
    await get_stats_by_phrase(self, chan, src, msg, happy, 'happiest')

async def saddest(self, chan, src, msg):
    sad = [':(', ':/', ':|', ';-;', ';_;', ';(', ':-(', ';-(',
        ':^(', ';^(', ':-/', ':-|', ';-/', ';-|', '=(', '=/',
        '=|', ':\'(', ':V', ':c']
    await get_stats_by_phrase(self, chan, src, msg, sad, 'saddest')

async def angriest(self, chan, src, msg):
    curses = ['darn', 'dang', 'damn', 'shit', 'fuck', 'fck', 'f*ck',
        'dick', 'moron', 'bitch', 'cunt'] # need more curse words!
    await get_stats_by_phrase(self, chan, src, msg, curses, 'angriest')

commands = {
    'noisiest': noisiest,
    'happiest': happiest,
    'saddest':  saddest,
    'angriest': angriest
}

async def usrstats_handle(self, chan, src, msg):
    msg = msg.split(' ')
    if len(msg) < 1 or not msg[0] in commands:
        await out.msg(self, modname, chan, [self.err_invalid_command])
        return
    await commands[msg.pop(0)](self, chan, src, ' '.join(msg))

async def init(self):
    self.handle_cmd['usrstats'] = usrstats_handle
    self.help['usrstats'] = ['usrstats - display statistics on various users (more for subcommands)', 'usrstats subcommands: noisiest happiest saddest angriest']
    self.help['usrstats noisiest'] = ['usrstats noisiest [chan] - get the top talkers for [chan] (default: current)']
    self.help['usrstats happiest'] = ['usrstats happiest [chan] - get the users who type "lol", "lmao", ":)", ":D", etc in their messages the most on [chan]. (default: current)']
    self.help['usrstats saddest'] = ['usrstats saddest [chan] - get the users who type ":/", ":(", etc in their messages the most on [chan]. (default: current)']
    self.help['usrstats angriest'] = ['usrstats angriest [chan] - get the users who curse the most on [chan]. (default: current)']
