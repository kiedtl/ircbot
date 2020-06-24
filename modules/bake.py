import common
import dataset
import random

from common import modname
from common import modname
module_name = 'oven'

async def purge(self, c, n, m):
    if not await self.is_admin(n):
        await self.message(c, '{} insufficient priviliges'
            .format(modname(module_name)))
        return
    if len(m) < 1:
        await self.message(c, '{} need username.'
            .format(modname(module_name)))
        return
    inv = self.db['inv']
    inv.delete(name=m)
    await self.message(c, '{} done'
        .format(modname(module_name)))

async def cheat(self, c, n, m):
    if not await self.is_admin(n):
        await self.message(c, '{} insufficient priviliges'
            .format(modname(module_name)))
        return
    m = m.split(' ')
    if len(m) < 2:
        await self.message(c, '{} need username and item.'
            .format(modname(module_name)))
        return
    inv = self.db['inv']
    inv.insert(dict(name=m[0], item=m[1]))
    await self.message(c, '{} done'
        .format(modname(module_name)))

async def give(self, c, n, m):
    m = m.split(' ')
    if len(m) < 2:
        await self.message(c, '{} you can\'t give air!'
            .format(modname(module_name)))
    inv = self.db['inv']
    its = inv.find_one(name=n, item=m[1])
    if its == None:
        await self.message(c, '{} you don\'t have that!'
            .format(modname(module_name)))
    inv.delete(id=its['id'])
    inv.insert(dict(name=m[0], item=its['item']))
    await self.message(c, '{} you gave {} a {}!'
        .format(modname(module_name), m[0], m[1]))

async def info(self, c, n, m):
    query = m.split(' ')[0]
    if len(m) < 1:
        await self.message(c, '{} need item name'
            .format(modname(module_name)))
        return
    inv = self.db['inv']
    items = [ i['item'] for i in inv.find(item = query) ]

    instances = len(items)
    price = 0
    if query in self.bakedGoods:
        price = self.bakedGoods[query] / 10

    await self.message(c, '{} there exist {} {}s, each with a value of ${}'
        .format(modname(module_name), instances, query, price))

async def bake(self, c, n, m):
    if len(m) < 1:
        await self.message(c, '{} you can\'t bake air!'
            .format(modname(module_name)))
        return
    inv = self.db['inv']
    its = (inv.find_one(name=n, item=m))
    if its == None:
        await self.message(c, '{} you don\'t have any {}'
            .format(modname(module_name), m))
        return

    # if item has value, use that, else use a okay value
    if m in list(self.bakedGoods.keys()):
        value = self.bakedGoods[m]
    else:
        value = 7

    # consume the item
    inv.delete(id=its['id'])

    # oooo randomize what will pop out
    value += random.uniform(-20, 20)

    # choose the output
    while value not in list(self.bakedPrice.keys()):
        value = int(value - 1)
        if value < 0:
            await self.message(c, '{} the oven begins to smoke...'
                .format(modname(module_name)))
            return

    newitem = self.bakedPrice[value]

    inv.insert(dict(name=n, item=newitem))

    await self.message(c, 'You bake your {}, and out pops a {}!'.format(m, newitem))

async def invsee(self, c, n, m):
    m = m.split(' ')[0]
    if len(m) < 1:
        m = n.strip()
    inv = self.db['inv']
    it = [ i['item'] for i in inv.find(name = m) ]
    if len(it) < 1:
        await self.message(c, 'You look in your oven and see nothing.')
    else:
        price = sum([self.bakedGoods[i]
            for i in it if i in self.bakedGoods]) / 10
        itemstats = {}
        for i in it:
            if not i in itemstats:
                itemstats[i] = 0
            itemstats[i] += 1
        output = 'You look in the oven and see: '
        for i in sorted(itemstats.items(), key=lambda i: i[1], reverse=True):
            output += f'{i[0]} (x{i[1]}), '
        output += f'with a combined value of ${price}'
        await self.message(c, output)

async def generate(self, c, n, m):
    if int(random.uniform(0, 30)) == 1:
        inv = self.db['inv']
        inv.insert(dict(name = n,
            item = random.choice(list(self.bakedGoods.keys()))))
        qed = self.db['qed']
        if qed.find_one(name=n) == None:
            qed.insert(dict(name=n))

async def init(self):
    self.db = dataset.connect('sqlite:///database.db')

    # todo: move all cmds to subcommands of 'ov'
    self.cmd['info'] = info
    self.cmd['bake'] = bake
    self.cmd['cheat'] = cheat
    self.cmd['inv'] = invsee
    self.cmd['items'] = invsee
    self.cmd['goods'] = invsee
    self.cmd['purge'] = purge
    self.cmd['give'] = give

    self.handle_raw['genGoods'] = generate

    self.help['info'] = ['info <item> - get info for item']
    self.help['bake'] = ['bake <item> - bake some stuff']
    self.help['cheat'] = ['cheat <user> <item> - you are bad if you use it']
    self.help['items'] = ['items|inv|goods [user] - show the stuff in your inventory']
    self.help['purge'] = ['purge <user> - clear someone\'s inventory']
    self.help['give'] = ['give <user> <item> - give someone something from your inventory']

    self.bakedGoods = {
        nohighlight('khuxkm'): -1,
        nohighlight('jan6'):    3,

        'poison':   -10,
        'roadkill': -3,
        'garbage':  -2,
        'skeleton': -2,
        'raw meat': -1,
        'spam':     0,
        'grass':    6,
        'flour':    7,
        'pizza':    8,
        'pancake':  12,
        'water':    15,
        'ration':   20,
        'egg':      20,
        'rice':     29,
        'bread':    30,
        'pie':      31,
        'bird':     32,
        'tortilla': 35,
        'cookie':   44,
        'cheese':   50,
        'sandwich': 55,
        'wafer':    56,
        'ducc':     200,
    }

    self.bakedPrice = dict((v,k) for k,v in self.bakedGoods.items())
