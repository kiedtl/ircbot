import common, dataset
import out, random, re

modname = 'karma'
is_karma = re.compile('(^[+-]{2}\(?[\S\W]+\)?$)|(^\(?[\S\W]+\)?[+-]{2}$)')
target_find = re.compile('([+-]{2})?\(?([^()+-]+)\)?([+-]{2})?')

async def filterkarma(self, chan, src, msg):
    if not is_karma.match(msg):
        return

    lo, target, ro = (target_find.findall(msg))[0]
    op = lo or ro

    # users' shouldn't be able to set
    # their own karma
    if src == target:
        return

    entry = self.karmadb.find_one(name=target)
    if entry == None:
        karma = 0
    else:
        self.karmadb.delete(id = entry['id'])
        karma = entry['amount']

    if op == '++':
        karma += 1
    elif op == '--':
        karma -= 1

    self.karmadb.insert(dict(name=target, amount=karma))

async def listkarma(self, chan, src, msg):
    entry = self.karmadb.find_one(name=msg)
    if entry == None or entry['amount'] == 0:
        await out.msg(self, modname, chan, [f'{msg} has 0 karma...'])
    else:
        num = entry['amount']
        await out.msg(self, modname, chan, [f'{msg} has {num} karma!'])

async def init(self):
    self.handle_raw['filterkarma'] = filterkarma
    self.karmadb = dataset.connect('sqlite:///dat/pnts.db')['karma']

    self.cmd['karma'] = listkarma

    self.help['karma'] = ['karma [thing] - get karma for thing. use <thing>++ or ++<thing> to set karma.']
