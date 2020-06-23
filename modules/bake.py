import dataset
import random

async def purge(self, c, n, m):
    if not await self.is_admin(n):
        await self.message(c,'{} was a bad bad bad. {} got sucked into the oven'.format(n,n))
    if len(m) < 1:
        await message(c, 'i refuse.')
        return
    inv = self.db['inv']
    inv.delete(name=m)
    await self.message(c,'ok lel')

async def cheat(self, c, n, m):
    if not await self.is_admin(n):
        await self.message(c,'{} was a bad bad bad. {} got sucked into the oven'.format(n,n))
    m = m.split(' ')
    if len(m) < 2:
        await message(c, 'i refuse.')
        return
    inv = self.db['inv']
    inv.insert(dict(name=m[0], item=m[1]))
    await self.message(c,'ok il allow this once')

async def give(self, c, n, m):
    m = m.split(' ')
    if len(m) < 2:
        await self.message(c, 'dummy thicc you cant give air!')
    inv = self.db['inv']
    its = inv.find_one(name=n, item=m[1])
    if its == None:
        await self.message(c, 'dummy thicc you cant trick me!')
    inv.delete(id=its['id'])
    inv.insert(dict(name=m[0], item=its['item']))
    await self.message(c, 'you gave {} a {}!'.format(m[0], m[1]))

async def bake(self, c, n, m):
    if len(m) < 1:
        await self.message(c, 'Dummy thicc you cant bake air!')
        return
    inv = self.db['inv']
    its = (inv.find_one(name=n, item=m))
    if its == None:
        await self.message(c, 'You dont have any {}'.format(m[:10]))
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
            await self.message(c, 'you notice some smoke, shouldint have put that {} in the oven!'.format(m))
            return

    newitem = self.bakedPrice[value]

    inv.insert(dict(name=n, item=newitem))

    await self.message(c, 'You bake your {}, and out pops a {}!'.format(m, newitem))

async def invsee(self, c, n, m):
    if len(m) < 1:
        m = n.strip()
    inv = self.db['inv']
    it = [ i['item'] for i in inv.find(name=m) ]
    if len(it) < 1:
        await self.message(c, 'you look through your kitchen and see nothing')
    else:
        await self.message(c, 'you look through your kitchen and see {}, with a combined value of ${}'.format(' '.join(it), sum([self.bakedGoods[i] for i in it if i in self.bakedGoods])/10))
        self.timeout += len(' '.join(it))/300

async def generate(self, c, n, m):
    if int(random.uniform(0,30)) == 1:
        inv = self.db['inv']
        inv.insert(dict(name=n, item=random.choice(list(self.bakedGoods.keys()))))
        qed = self.db['qed']
        if qed.find_one(name=n) == None:
            qed.insert(dict(name=n))

async def init(self):
    # the share directory would have to be
    # created if it doesn't exist
    self.db = dataset.connect('sqlite:///database.db')

    # todo: move all cmds to subcommands of 'ov'
    self.cmd['bake'] = bake
    self.cmd['cheat'] = cheat
    self.cmd['inv'] = invsee
    self.cmd['items'] = invsee
    self.cmd['goods'] = invsee
    self.cmd['purge'] = purge
    self.cmd['give'] = give

    self.handle_raw['genGoods'] = generate

    self.help['bake'] = ['bake <item> - bake some stuff']
    self.help['cheat'] = ['cheat <user> <item> - you are bad if you use it']
    self.help['items'] = ['items|inv|goods [user] - show the stuff in your inventory']
    self.help['purge'] = ['purge <user> - clear someone\'s inventory']
    self.help['give'] = ['give <user> <item> - give someone something from your inventory']

    self.bakedGoods = {
        'ducc': 200,
        'cheese': 50,
        'grass': 6,
        'flour': 10,
        'bread': 30,
        'tortilla': 35,
        'egg': 20,
        'bird': 32,
        'roadkill': 4,
        'ration': 20,
        'raw meat': 5,
        'skeleton': 1,
        'pizza': 15,
        'cookie': 44,
        'pancake': 12,
        'rice': 29,
        'sandwich':55,
        'wafer': 56,
        'pie': 31,
    }

    self.bakedPrice = dict((v,k) for k,v in self.bakedGoods.items())
