import common
import dataset
import random

from common import modname
from common import nohighlight
module_name = 'oven'
default_price = 7

async def purge(self, c, n, m):
    if not await self.is_admin(n):
        await self.message(c, '{} insufficient priviliges'
            .format(modname(module_name)))
        return
    if len(m) < 1:
        await self.message(c, '{} need username.'
            .format(modname(module_name)))
        return
    inv = self.ovendb['inv']
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
    inv = self.ovendb['inv']
    inv.insert(dict(name=m[0], item=m[1]))
    await self.message(c, '{} done'
        .format(modname(module_name)))

async def give(self, c, n, m):
    m = m.split(' ')
    if len(m) < 2:
        await self.message(c, '{} you can\'t give air!'
            .format(modname(module_name)))
    inv = self.ovendb['inv']
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
    inv = self.ovendb['inv']
    items = [ i['item'] for i in inv.find(item = query) ]

    instances = len(items)
    price = 0
    if query in self.bakedGoods:
        price = self.bakedGoods[query] / 10
    total_price = instances * price

    await self.message(c, '{} there exist {} {}s, each with a value of ${:.2f} and a combined value of ${:.2f}'
        .format(modname(module_name), instances,
            query, price, total_price))

async def owners(self, c, n, m):
    query = m.split(' ')[0]
    if len(m) < 1:
        await self.message(c, '{} need item name'
            .format(modname(module_name)))
        return
    inv = self.ovendb['inv']

    total = 0
    stats = {}
    for item in list(inv.find(item = query)):
        if not item['name'] in stats:
            stats[item['name']] = 0
        stats[item['name']] += 1
        total += 1

    output = ''
    ctr = 0
    until = 7
    for i in sorted(stats.items(), key=lambda i: i[1], reverse=True):
        if ctr == until:
            break
        percentage = (i[1] * 100) / total
        output += ('{} (×{}, {:.0f}%), '
            .format(nohighlight(i[0]), i[1], percentage))
        ctr += 1

    output = output[:-2] # trim ', '
    await self.message(c, '{} top {} owners: {}'
        .format(modname(module_name), query, output))

async def richest(self, c, n, m):
    inv = self.ovendb['inv']

    total = 0
    stats = {}
    for item in list(inv.find()):
        price = default_price
        if item['item'] in self.bakedGoods:
            price = self.bakedGoods[item['item']] / 10

        if not item['name'] in stats:
            stats[item['name']] = 0
        stats[item['name']] += price
        total += price

    output = ''
    ctr = 0
    until = 7
    for i in sorted(stats.items(), key=lambda i: i[1], reverse=True):
        if ctr == until:
            break
        percentage = (i[1] * 100) / total
        output += ('{} (${:.2f}, {:.1f}%), '
            .format(nohighlight(i[0]), i[1], percentage))
        ctr += 1

    output = output[:-2] # trim ', '
    await self.message(c, '{} richest users: {} (total wealth: ${:.2f})'
        .format(modname(module_name), output, total))

# TODO: combine multiple loops for speedup
async def bake(self, c, n, m):
    if len(m) < 1:
        await self.message(c, '{} you can\'t bake air!'
            .format(modname(module_name)))
        return

    inv = self.ovendb['inv']
    input = m.split()
    #await self.message(c, f'DEBUG: bakign items: {input}')

    for thing in input:
        its = inv.find_one(name=n, item=thing)

        if its == None:
            await self.message(c, '{} you don\'t have any {}'
                .format(modname(module_name), thing))
            return

        # if they try to bake a ducc, destroy
        # their stuff >:(
        # if it's a bomb, blow up.
        if thing == 'ducc' or thing == 'bomb':
            if thing == 'ducc':
                await self.message(c, '{} {} brutally murders the ducc amidst its terrified quacks and stuffs it into the oven.'
                    .format(modname(module_name), n))
            await self.message(c, '{} the oven explodes!'
                .format(modname(module_name)))
            inv.delete(name=n)
            return

        # consume the item
        for thing in input:
            inv.delete(id = its['id'])


    # if item has value, use that, else use a okay value
    values = []
    for thing in input:
        if thing in list(self.bakedGoods.keys()):
            values.append(self.bakedGoods[thing])
        else:
            values.append(default_price)

    # oooo randomize what will pop out
    sum_value = sum(values)
    avg_value = sum_value / len(values)
    #await self.message(c, f'DEBUG: sum={sum_value}, avg={avg_value}')
    output_value = random.uniform(
        min(sum_value, avg_value),
        max(sum_value, avg_value))

    # choose the output
    prices = list(self.bakedPrice.keys())
    min_price = min(prices)
    while output_value not in prices:
        output_value = int(output_value - 1)
        if output_value < min_price:
            await self.message(c, '{} the oven begins to smoke...'
                .format(modname(module_name)))
            return

    newitem = self.bakedPrice[output_value]
    inv.insert(dict(name=n, item=newitem))

    await self.message(c, f'{modname(module_name)} You bake your items, and out pops a {newitem}!')

async def invsee(self, c, n, m):
    m = m.split(' ')[0]
    if len(m) < 1:
        m = n.strip()
    inv = self.ovendb['inv']
    it = [ i['item'] for i in inv.find(name = m) ]
    if len(it) < 1:
        await self.message(c, f'{modname(module_name)} You look in the oven and see nothing.')
    else:
        price = sum([self.bakedGoods[i]
            for i in it if i in self.bakedGoods]) / 10
        itemstats = {}
        for i in it:
            if not i in itemstats:
                itemstats[i] = 0
            itemstats[i] += 1
        output = f'{modname(module_name)} You look in the oven and see: '
        for i in sorted(itemstats.items(), key=lambda i: i[1], reverse=True):
            output += f'{i[0]} (×{i[1]}), '
        output += f'with a combined value of ${price:.2f}'
        await self.message(c, output)

async def generate(self, c, n, m):
    if int(random.uniform(1, 50)) == 1:
        inv = self.ovendb['inv']

        # ensure that items with a high price
        # have a very low chance of being given
        # items with a low or negative price
        # have a high chance of being given
        choices = []
        for item in self.bakedGoods:
            # probability of getting an item
            prob = int(((max(list(self.bakedPrice.keys())) + 2)
                - abs(self.bakedGoods[item])))
            for i in range(0, prob):
                choices.append(item)
        random.shuffle(choices)

        inv.insert(dict(name = n,
            item = random.choice(choices)))
        qed = self.ovendb['qed']
        if qed.find_one(name=n) == None:
            qed.insert(dict(name=n))

commands = {
    'info': info,
    'bake': bake,
    'cheat': cheat,
    'inv': invsee,
    'items': invsee,
    'goods': invsee,
    'purge': purge,
    'give': give,
    'owners': owners,
    'richest': richest
}

async def ov_handle(self, chan, src, msg):
    msg = msg.split(' ')
    if len(msg) < 1 or not msg[0] in commands:
        await common.msg(self, chan, '{} {}'
            .format(modname(module_name), self.err_invalid_command))
        return
    await commands[msg.pop(0)](self, chan, src, ' '.join(msg))

async def init(self):
    self.ovendb = dataset.connect('sqlite:///dat/oven.db')

    self.cmd['ov'] = ov_handle
    self.handle_raw['genGoods'] = generate

    self.help['ov'] = ['ov <command> - a worthless ripoff of badger by lickthecheese and Yours Truly (more for subcommands)', 'ov subcommands: info bake cheat items|inv|goods purge give owners richest']
    self.help['ov info'] = ['info <item> - get info for item']
    self.help['ov bake'] = ['bake <item> - bake some stuff']
    self.help['ov cheat'] = ['cheat <user> <item> - you are bad if you use it']
    self.help['ov items'] = ['items|inv|goods [user] - show the stuff in your inventory']
    self.help['ov inv'] = self.help['ov items']
    self.help['ov goods'] = self.help['ov items']

    self.help['ov purge'] = ['purge <user> - clear someone\'s inventory']
    self.help['ov give'] = ['give <user> <item> - give someone something from your inventory']
    self.help['ov owners'] = ['owners <item> - see which users own an item']
    self.help['ov richest'] = ['richest - see which users own the most valuable items']

    self.bakedGoods = {
        nohighlight('khuxkm'): 10,
        nohighlight('jan6'):   10,

        'bomb':      -200,
        'ricin':      -40,
        'nightshade': -20,
        'foxglove':    -7,
        'roadkill':    -3,
        'garbage':     -2,
        'skeleton':    -2,
        'bone':        -1,
        'spam':       0.7,
        'grass':        4,
        'flour':        3,
        'pizza':        8,
        'pancake':     12,
        'water':       15,
        'ration':      20,
        'egg':         20,
        'rice':        29,
        'bread':       30,
        'pie':         31,
        'bird':        32,
        'tortilla':    35,
        'cookie':      44,
        'cheese':      50,
        'sandwich':    55,
        'wafer':       56,
        'ducc':        200,
    }

    self.bakedPrice = dict((v,k) for k,v in self.bakedGoods.items())
