import os
from common import modname, nohighlight, loadlogs
module_name = 'chan stats'

async def totalmsgs(self, chan, src, msg):
    channels = 'all'
    logfiles = []
    for i in [s for s in os.listdir('chans') if '#' in s]:
        logfiles.append(i)
    if len(msg) > 0:
        channels = ', '.join(msg.split(' '))
        logfiles = msg.split(' ')

    logs = []
    for logfile in logfiles:
        try:
            logs += loadlogs(chan)
        except:
            await self.message(chan, '{} error opening log file'
                .format(modname(module_name)))
            return
    await self.message(chan, '{} {:,} total messages for {} channel(s)'
            .format(modname(module_name), len(logs), channels))


commands = {
    'totalmsgs': totalmsgs
}

async def chanstats_handle(self, chan, source, msg):
    msg = msg.split(' ')
    if len(msg) < 1 or not msg[0] in commands:
        await self.message(chan, '{} invalid command'
            .format(modname(module_name)))
        return
    await commands[msg.pop(0)](self, chan, source, ' '.join(msg))

async def init(self):
    self.cmd['chanstats'] = chanstats_handle
    self.help['chanstats'] = ['display statistics of various channels (more for subcommands)', 'chanstats subcommands: totalmsgs']
    self.help['chanstats totalmsgs'] = ['chanstats totalmsgs [chans] - get total messages for [chans]. [chans] defaults to all channels.']
