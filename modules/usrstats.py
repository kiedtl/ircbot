from common import modname
module_name = 'user stats'

async def noisiest(self, chan, src, msg):
    stats = {}

    if len(msg) < 1:
        msg = '1'

    try:
        until = int(msg)
    except:
        until = 3

    # prevent spam
    if until > 10:
        until = 10

    logf = ''
    try:
        logf = open('chans/{}.log'.format(chan))
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

    ctr = 0
    for i in sorted(stats.items(), key=lambda i: i[1], reverse=True):
        if ctr == until:
            break
        await self.message(chan, '{} {}: {} messages'
            .format(modname(module_name), i[0], i[1]))
        ctr += 1

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
