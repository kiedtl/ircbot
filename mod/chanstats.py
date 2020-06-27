import os
from common import modname, nohighlight, loadlogs
module_name = 'chan stats'

async def totalmsgs(self, chan, src, msg):
    channels = 'all known'
    logfiles = []
    if len(msg) > 0:
        channels = ', '.join(msg.split(' '))
        logfiles = msg.split()
    else:
        for i in [s for s in os.listdir('irc') if '#' in s]:
            logfiles.append(i)

    logs = []
    for logfile in logfiles:
        try:
            logs += loadlogs(logfile)
        except:
            await self.message(chan, '{} {}: {}'
                .format(modname(module_name),
                    self.err_invalid_logfile, logfile))
            return

    await self.message(chan, '{} {:,} total messages for {} channel(s)'
            .format(modname(module_name), len(logs), channels))

async def totalnicks(self, chan, src, msg):
    channels = 'all known'
    logfiles = []
    if len(msg) > 0:
        channels = ', '.join(msg.split(' '))
        logfiles = msg.split()
    else:
        for i in [s for s in os.listdir('irc') if '#' in s]:
            logfiles.append(i)

    stats = {}

    for logfile in logfiles:
        logs = []
        try:
            logs = loadlogs(logfile)
        except:
            await self.message(chan, '{} {}: {}'
                .format(modname(module_name),
                    self.err_invalid_logfile, logfile))
            return

        for log in logs:
            data = log.split()
            if len(data) < 2:
                continue
            nick = data[1]
            if not nick in stats:
                stats[nick] = 0
            stats[nick] += 1

    await self.message(chan, '{} {:,} total unique nicks for {} channel(s)'
            .format(modname(module_name), len(stats), channels))

commands = {
    'totalmsgs': totalmsgs,
    'totalnicks': totalnicks
}

async def chanstats_handle(self, chan, source, msg):
    msg = msg.split(' ')
    if len(msg) < 1 or not msg[0] in commands:
        await self.message(chan, '{} {}'
            .format(modname(module_name), self.err_invalid_command))
        return
    await commands[msg.pop(0)](self, chan, source, ' '.join(msg))

async def init(self):
    self.cmd['chanstats'] = chanstats_handle
    self.help['chanstats'] = ['display statistics of various channels (more for subcommands)', 'chanstats subcommands: totalmsgs']
    self.help['chanstats totalmsgs'] = ['chanstats totalmsgs [chans] - get total messages for [chans]. [chans] defaults to all channels.']
