# backlogger
# stores messages for modules such
# as :pig and :owo and logs them
# for irc statistics

from datetime import datetime

async def backlogger(self, chan, src, msg):
    if chan not in self.backlog:
        self.backlog[chan] = []
    if chan not in self.logfiles:
        logpath = 'chans/{}.log'.format(chan)
        print('[logger] opening logfile {}'.format(logpath))
        self.logfiles[chan] = open(logpath, 'a')

    # store in logfile
    now = datetime.now()
    time = datetime.strftime(now, '%d%m%y%H%M')
    self.logfiles[chan].write('{} {} {}\n'.format(time, src, msg))
    self.logfiles[chan].flush()

    # don't store in backlog if msg is a command
    if src == self.nickname:
        return
    if msg[:len('|| ')] == '|| ':
        # it's a :sed command alias
        return
    if msg[:len(self.prefix)] == self.prefix:
        cmd = msg[len(self.prefix):]
        cmd = cmd.split(' ')[0]
        if cmd in self.cmd:
            return

    self.backlog[chan].append([src, msg])

    # flush backlog if its size exceeds 1024
    if len(self.backlog[chan]) > 1024:
        del self.backlog[chan][:-512]

async def init(self):
    self.backlog = {}
    self.logfiles = {}
    self.raw['backlog'] = backlogger
