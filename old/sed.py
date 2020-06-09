import common, re

async def filtersed(self, chan, src, msg):
    """detect if message is sed command"""
    is_sed = re.compile('^\|[a-zA-Z]*\|\ .*$')
    if is_sed.match(msg):
        usr = re.findall(r'^\|([a-zA-Z]*)\|', msg)[0]
        msg = msg[(len(usr) + 2):]
        if len(usr) == 0:
            usr = src
        await sed(self, chan, usr, msg)

async def sed(self, chan, src, msg):
    sedmsg = []

    # find last message by user
    for i in self.backlog[chan]:
        if i[0] == src:
            sedmsg = i

    if len(sedmsg) == 0:
        await self.message(chan, self.err_backlog_too_short)
        return

    cmd = ['sed', '-e', ''.join(msg)]
    res = common.run(self, cmd, sedmsg[1])
    await self.message(chan, '<{}> {}'.format(sedmsg[0], res))

async def init(self):
    self.raw['filtersed'] = filtersed
    self.cmd['sed'] = sed
    self.help['sed'] = ['sed - an improved version of the sedbot. (more for usage)',
        'syntax: |<user>| <expr>. note that <user> can be omitted if the command is issued by the same user. example: |spacehare| s/teh/the/g']
