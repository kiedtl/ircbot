import datetime, random

async def logger(self, chan, src, msg):
    date = datetime.datetime.now()
    time = datetime.datetime.strftime(date, '%d%m%y%H%M')

    if chan not in self.log:
        self.log[chan] = []

    self.log[chan].append([time, src, msg])

    if len(self.log[chan]) > 512:
        logf = open('chans/{}.log'.format(chan), 'a')
        for i in self.log[chan]:
            logf.write('{} {} {}\n'
                    .format(i[0], i[1], i[2]))
        logf.close()
        self.log[chan] = []

async def init(self):
    self.log = {}
    self.raw['logger'] = logger
