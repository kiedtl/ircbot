from common import modname, nohighlight
module_name = 'user stats'

async def noisiest(self, chan, src, msg):
    stats = {}
    total = 0

    targetchan = chan
    if len(msg) > 0 and msg[:1] == '#':
        targetchan = msg

    logf = ''
    try:
        logf = open('chans/{}.log'.format(targetchan))
    except:
        await self.message(chan, '{} error opening log file'
            .format(modname(module_name)))
        return

    logs = logf.read().split('\n')
    for line in logs:
        data = line.split(' ', 3)
        if len(data) < 3:
            continue
        time = data[0]
        user = data[1]
        mesg = data[2]
        if not user in stats:
            stats[user] = 0
        stats[user] += 1
        total += 1

    output = ''
    ctr = 0
    until = 3
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

commands = {
    'noisiest': noisiest
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
    self.help[''] = ['']
