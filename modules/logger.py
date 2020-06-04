import datetime, random

async def logger(self, chan, src, msg):
    date = datetime.datetime.now()
    time = datetime.datetime.strftime(date, '%d%m%y%H%M')
    if chan not in self.logfiles:
        self.logfiles[chan] = open('chans/{}.log'
            .format(chan), 'a')
    self.logfiles[chan].write('{} {} {}\n'.format(time, src, msg))

async def init(self):
    self.logfiles = {}
    self.raw['logger'] = logger
