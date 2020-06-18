from common import modname, nohighlight
module_name = 'user stats'

# TODO: move to common
async def get_all_logs(chan, msg):
    logf = open('chans/{}.log'.format(chan))
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

async def noisiest(self, chan, src, msg):
    stats = {}
    total = 0
    logs = []
    targetchan = chan
    if len(msg) > 0 and msg[:1] == '#':
        targetchan = msg

    try:
        logs = await self.get_all_logs(targetchan, msg)
    except:
        await self.message(chan, '{} error opening log file'
            .format(modname(module_name)))
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
    await self.message(chan, '{} top talkers at {}: {}'
        .format(modname(module_name), targetchan, output))

async def happiest(self, chan, src, msg):
    stats = {}

    targetchan = chan
    if len(msg) > 0 and msg[:1] == '#':
        targetchan = msg

    logs = []
    try:
        logs = await get_all_logs(targetchan, msg)
    except:
        await self.message(chan, '{} error opening log file'
            .format(modname(module_name)))
        return

    happy = ['lol', 'lmao', ':)', ':-)', ':^)', ':D' ':-D', ';)', 'c:']
    for item in logs:
        if any(phrase in item['msg'] for phrase in happy):
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
    await self.message(chan, '{} happiest people at {}: {}'
        .format(modname(module_name), targetchan, output))

async def saddest(self, chan, src, msg):
    stats = {}

    targetchan = chan
    if len(msg) > 0 and msg[:1] == '#':
        targetchan = msg

    logs = []
    try:
        logs = await get_all_logs(targetchan, msg)
    except:
        await self.message(chan, '{} error opening log file'
            .format(modname(module_name)))
        return

    sad = [':(', ':/', ':|', ';-;', ';_;', ';(', ':-(', ';-(',
        ':^(', ';^(', ':-/', ':-|', ';-/', ';-|', '=(', '=/',
        '=|', ':\'(']
    for item in logs:
        if any(phrase in item['msg'] for phrase in sad):
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
    await self.message(chan, '{} saddest people at {}: {}'
        .format(modname(module_name), targetchan, output))

commands = {
    'noisiest': noisiest,
    'happiest': happiest,
    'saddest':  saddest
}

async def usrstats_handle(self, chan, source, msg):
    msg = msg.split(' ')
    if len(msg) < 1 or not msg[0] in commands:
        await self.message(chan, '{} invalid command'
            .format(modname(module_name)))
        return
    await commands[msg.pop(0)](self, chan, source, ' '.join(msg))

async def init(self):
    self.cmd['usrstats'] = usrstats_handle
    self.help['usrstats'] = ['usrstats - display statistics on various users (more for subcommands)', 'usrstats subcommands: noisiest happiest saddest']
    self.help['usrstats noisiest'] = ['usrstats noisiest [chan] - get the top talkers for [chan] (default: current)']
    self.help['usrstats happiest'] = ['usrstats happiest [chan] - get the users who type "lol", "lmao", ":)", ":D", etc in their messages the most on [chan]. (default: current)']
    self.help['usrstats saddest'] = ['usrstats saddest [chan] - get the users who type ":/", ":(", etc in their messages the most on [chan]. (default: current)']
