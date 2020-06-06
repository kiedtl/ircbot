import common

async def sed(self, chan, src, msg):
    sedmsg = []

    # find last message by user
    for i in self.backlog[chan]:
        if i[0] == src:
            sedmsg = i

    cmd = ['sed', '-e', ''.join(msg)]
    print('DEBUG: cmd={}'.format(cmd))
    res = common.run(self, cmd, sedmsg[1])
    await self.message(chan, '<{}> {}'.format(sedmsg[0], res))

async def init(self):
    self.cmd['sed'] = sed
    self.help['sed'] = ['']
