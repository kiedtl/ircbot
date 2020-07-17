import time, dataset, out, random
from common import nohighlight

modname = 'oven'
DEFAULT_PRICE = 7

ovendb   = dataset.connect('sqlite:///dat/oven.db')
oveninv  = ovendb['inv']
ovenqed  = ovendb['qed']

# TODO: add the rest of msgs here
msgs = {
    'INV_EMPTY': 'you look into the oven and see nothing',
    'BAKE_RESULT': 'you bake your items, and out pops a {}!',
    'BAKE_SMOKING': 'the oven begins to smoke...',
    'BAKE_EXPLODE': 'the oven explodes!',
    'BAKE_MURDER': '{} brutally murders the ducc amidst its terrified quaccs and stuffs it into the oven.',
    'BAKE_NEED_TWO': 'you need at least two items',
    'DONT_HAVE_ENOUGH': 'you don\'t have enough of {}',
    'DONT_HAVE_ANY': 'you don\'t have any {}',
    'USER_NOT_FOUND': 'that user doesn\'t exist',
    'FOOD_NOM_NOM': 'nom nom nom',
    'DUCK_GONE_GONE': 'you lose your hold on the ducc and it flies away!',
    'POIS_BOOM_BOOM': 'not a good idea...', # poison
}

baked_goods = {
    nohighlight('khuxkm'): 10,
    nohighlight('jan6'):   10,

    'bomb':        -400,
    'roadkill':     -10,
    'bone':         -10,
    'spam':           2,
    'grass':          4,
    'flour':          8,
    'pizza':         10,
    'pancake':       28,
    'water':         20,
    'ration':        38,
    'egg':           30,
    'rice':          40,
    'bread':         40,
    'pie':           58,
    'bird':          50,
    'tortilla':      65,
    'cookie':        74,
    'cheese':        80,
    'sandwich':      95,
    'wafer':        100,
    'ducc':         400,
}

baked_price = dict((v, k)
    for k, v in baked_goods.items())


class NotEnoughItems(Exception):
    """
    There isn't enough of an item in
    someone's inventory.
    """
    pass


class TriedBakeDucc(Exception):
    """
    Someone tried to bake a ducc!
    """
    pass

class TriedBakeBomb(Exception):
    """
    Someone tried to bake a bomb!!
    """
    pass


class InventoryNotFound(Exception):
    """
    Someone tried to transfer an item,
    but the inventory doesn't exist.
    """
    pass


class SmokingOven(Exception):
    """
    The oven begins to smoke!
    """
    pass


def _get_price(item):
    if item in baked_goods:
        return baked_goods[item]
    else:
        return DEFAULT_PRICE


def _destroy_item(nick, item, count):
    """
    Destroy an item in a user's inventory.
    """
    found = list(oveninv.find(name=nick, item=item))

    if len(found) < count:
        raise NotEnoughItems(
            f'need {count} of {item}, found {len(found)}')

    oveninv.delete(
        id=[i['id'] for i in found[:count]])


def _create_item(nick, item, count):
    """
    Create an item and give it to a user.
    """
    for i in range(0, count):
        oveninv.insert(dict(name=nick, item=item))


def _transfer_item(giver, recipient, item, count):
    """
    Take item from <giver>'s inventory and place
    it into <recipient>'s inventory.
    """
    if ovenqed.find_one(name=recipient) == None:
        raise InventoryNotFound()

    found = list(oveninv.find(name=giver, item=item))

    if len(found) < count:
        raise NotEnoughItems(
            f'need {count} of {item}, found {len(found)}')

    for i in range(0, count):
        item = found[i]
        oveninv.delete(id=item['id'])
        oveninv.insert(
            dict(name=recipient, item=item['item']))


def _count_item(nick, item):
    """
    Check how many of <item> there exist in
    <nick>'s inventory.
    """
    found = oveninv.find(name=nick, item=item)
    return len(list(found))


def _bake_items(nick, items):
    for thing in items:
        found = _count_item(nick, thing)

        if found < items[thing]:
            raise NotEnoughItems(
                f'need {items[thing]} of {thing}, found {found}')

        if thing == 'ducc':
            raise TriedBakeDucc()
        elif thing == 'bomb':
            raise TriedBakeBomb()

    # if item has value, use that, else use a okay value
    values = []
    for thing in items:
        for i in range(0, items[thing]):
            values.append(_get_price(thing))

    # oooo randomize what will pop out
    sum_value = sum(values)
    avg_value = sum_value / len(values)
    output_value = random.uniform(sum_value,
        sum_value + avg_value)
    initial_output_value = output_value

    # choose the output
    min_price = min(baked_price.keys())
    max_price = max(baked_price.keys())
    while output_value not in list(baked_price.keys()):
        if initial_output_value < 0:
            output_value = int(output_value + 1)
        else:
            output_value = int(output_value - 1)
        if output_value < min_price or output_value > max_price:
            raise SmokingOven()
            return

    newitem = baked_price[output_value]

    _create_item(nick, newitem, 1)
    return newitem


async def purge(self, c, n, m):
    if len(m) < 1:
        await out.msg(self, modname, c, [f'need username'])
        return
    oveninv.delete(name=m)
    await out.msg(self, modname, c, [f'done'])


async def cheat(self, c, n, m):
    if len(m.split(' ')) < 2:
        await out.msg(self, modname, c, [f'need username and item.'])
        return

    data = m.split(' ')
    user = data[0]
    for thing in data[1:]:
        _create_item(user, thing, 1)
    await out.msg(self, modname, c, [f'done'])


async def give(self, c, n, m):
    m = m.split(' ')
    if len(m) < 2:
        await out.msg(self, modname, c, [f'you can\'t give air!'])
        return

    if _count_item(n, m[1]) < 1:
        await out.msg(self, modname, c,
            [msgs['DONT_HAVE_ANY'].format(m[1])])
        return

    try:
        _transfer_item(n, m[0], m[1], 1)
    except InventoryNotFound:
        await out.msg(self, modname, c,
            [msgs['USER_NOT_FOUND']])
        return

    receiver = nohighlight(m[0])
    await out.msg(self, modname, c,
        [f'you gave {receiver} a {m[1]}!'])


async def giveall(self, c, n, m):
    m = m.split(' ')
    if len(m) < 2:
        await out.msg(self, modname, c, [f'you can\'t give air!'])
        return

    itemcount = _count_item(n, m[1])

    if itemcount < 1:
        await out.msg(self, modname, c,
            [msgs['DONT_HAVE_ANY'].format(m[1])])
        return

    try:
        _transfer_item(n, m[0], m[1], itemcount)
    except InventoryNotFound:
        await out.msg(self, modname, c,
            [msgs['USER_NOT_FOUND']])
        return

    receiver = nohighlight(m[0])
    # TODO: pluralize properly
    await out.msg(self, modname, c,
        [f'you gave {receiver} your {m[1]}(s)!'])


async def info(self, c, n, m):
    query = m.split(' ')[0]
    if len(m) < 1:
        await out.msg(self, modname, c, [f'need item name'])
        return
    items = [ i['item'] for i in oveninv.find(item = query) ]

    instances = len(items)
    price = _get_price(query) / 10
    total_price = instances * price

    await out.msg(self, modname, c,
        [f'there exist {instances} {query}s, each with a value of ${price:.2f} and a combined value of ${total_price:.2f}'])


async def owners(self, c, n, m):
    query = m.split(' ')[0]
    if len(m) < 1:
        await out.msg(self, modname, c, [f'need item name.'])
        return

    total = 0
    stats = {}
    for item in list(oveninv.find(item = query)):
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
    await out.msg(self, modname, c, [f'top {query} owners: {output}'])


async def richest(self, c, n, m):
    total = 0
    stats = {}

    if len(m) > 0:
        results = oveninv.find(item=m)
    else:
        results = oveninv.find()

    for item in list(results):
        price = DEFAULT_PRICE
        if item['item'] in baked_goods:
            price = baked_goods[item['item']] / 10

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
    await out.msg(self, modname, c,
        [f'richest users: {output} (total wealth: ${total:,.2f})'])


async def recipe(self, c, n, m):
    _input = m.split()

    if len(_input) < 2:
        await out.msg(self, modname, c, [msgs['BAKE_NEED_TWO']])
        return

    items = {}
    for thing in _input:
        if not thing in items:
            items[thing] = 0
        items[thing] += 1

    try:
        newitem = _bake_items(n, items)
    except TriedBakeDucc:
        await out.msg(self, modname, c,
            ['baking a ducc?? how could you?!'])
        return
    except TriedBakeBomb:
        await out.msg(self, modname, c,
            ['baking bombs aren\'t a good idea...'])
        return
    except SmokingOven:
        await out.msg(self, modname, c,
            ['something doesn\'t seem right...'])
        return

    await out.msg(self, modname, c,
        [f'those items *might* give a {newitem}...'])


async def bake(self, c, n, m):
    _input = m.split()

    if len(_input) < 2:
        await out.msg(self, modname, c, [msgs['BAKE_NEED_TWO']])
        return

    items = {}
    for thing in _input:
        if not thing in items:
            items[thing] = 0
        items[thing] += 1

    # verify that they have enough items
    for thing in items:
        found = _count_item(n, thing)
        if found == 0:
            await out.msg(self, modname, c,
                [msgs['DONT_HAVE_ANY'].format(thing)])
            return
        elif found < items[thing]:
            await out.msg(self, modname, c,
                [msgs['DONT_HAVE_ENOUGH'].format(thing)])
            return

    try:
        newitem = _bake_items(n, items)
    except NotEnoughItems:
        pass # FIXME
    except TriedBakeDucc:
        await out.msg(self, modname, c,
            [msgs['BAKE_MURDER'].format(n)])
        await out.msg(self, modname, c, [msgs['BAKE_EXPLODE']])
        oveninv.delete(name=n)
        return
    except TriedBakeBomb:
        await out.msg(self, modname, c, [msgs['BAKE_EXPLODE']])
        oveninv.delete(name=n)
        return
    except SmokingOven:
        await out.msg(self, modname, c, [msgs['BAKE_SMOKING']])
        return

    # consume the item
    for item in items:
        _destroy_item(n, item, items[item])

    await out.msg(self, modname, c,
        [msgs['BAKE_RESULT'].format(newitem)])

async def bakeall(self, c, n, m):
    item = m.split()[0]

    if len(item) < 1:
        await out.msg(self, modname, c, ['need item'])
        return

    found = _count_item(n, item)
    if found == 0:
        await out.msg(self, modname, c,
            [msgs['DONT_HAVE_ANY'].format(item)])
        return
    elif found < 2:
        await out.msg(self, modname, c,
            [msgs['DONT_HAVE_ENOUGH'].format(item)])
        return

    items = { item: found }

    # TODO: pluralize properly
    await out.msg(self, modname, c, [f'baking {found} {item}s...'])

    try:
        newitem = _bake_items(n, items)
    except TriedBakeDucc:
        await out.msg(self, modname, c,
            [msgs['BAKE_MURDER'].format(n)])
        await out.msg(self, modname, c, [msgs['BAKE_EXPLODE']])
        oveninv.delete(name=n)
        return
    except TriedBakeBomb:
        await out.msg(self, modname, c, [msgs['BAKE_EXPLODE']])
        oveninv.delete(name=n)
        return
    except SmokingOven:
        await out.msg(self, modname, c, [msgs['BAKE_SMOKING']])
        return

    # consume the item
    for item in items:
        _destroy_item(n, item, items[item])

    await out.msg(self, modname, c,
        [msgs['BAKE_RESULT'].format(newitem)])

async def eat(self, c, n, m):
    if len(m) < 1:
        await out.msg(self, modname, c, [f'need item'])
        return

    item = m.split()[0]

    if _count_item(n, item) < 1:
        await out.msg(self, modname, c,
            [msgs['DONT_HAVE_ANY'].format(thing)])
        return

    if item == 'ducc':
        await out.msg(self, modname, c, [msgs['DUCK_GONE_GONE']])
    elif item == 'bomb' or _get_price(item) < 0:
        await out.msg(self, modname, c, [msgs['POIS_BOOM_BOOM']])
        return
    else:
        await out.msg(self, modname, c, [msgs['FOOD_NOM_NOM']])

    _destroy_item(n, item, 1)


async def invsee(self, c, n, m):
    m = m.split(' ')[0]
    if len(m) < 1:
        m = n.strip()

    it = [ i['item'] for i in oveninv.find(name = m) ]
    if len(it) < 1:
        await out.msg(self, modname, c, [msgs['INV_EMPTY']])
    else:
        price = sum([baked_goods[i]
            for i in it if i in baked_goods]) / 10
        itemstats = {}
        for i in it:
            if not i in itemstats:
                itemstats[i] = 0
            itemstats[i] += 1
        output = 'you look in the oven and see: '
        for i in sorted(itemstats.items(), key=lambda i: i[1], reverse=True):
            output += f'{i[0]} (×{i[1]}), '
        output += f'with a combined value of ${price:.2f}'
        await out.msg(self, modname, c, [output])


async def generate(self, c, n, m):
    if int(random.uniform(1, 50)) == 1:
        # ensure that items with a high price
        # have a very low chance of being given
        # items with a low or negative price
        # have a high chance of being given
        choices = []
        for item in baked_goods:
            # probability of getting an item
            prob = int(((max(list(baked_price.keys())) + 2)
                - abs(baked_goods[item])))
            for i in range(0, prob):
                choices.append(item)
        random.shuffle(choices)

        oveninv.insert(dict(name = n,
            item = random.choice(choices)))
        if ovenqed.find_one(name=n) == None:
            ovenqed.insert(dict(name=n))


async def ov_handle(self, c, src, msg):
    msg = msg.split()
    if len(msg) < 1:
        await out.msg(self, modname, c,
            [f'need subcommand (see :help ov)'])
        return
    if not msg[0] in commands and not msg[0] in admin_commands:
        await out.msg(self, modname, c, [self.err_invalid_command])
        return
    if msg[0] in admin_commands:
        if not await self.is_admin(src):
            await out.msg(self, modname, c,
                ['insufficient privileges'])
            return
        await admin_commands[msg.pop(0)](self, c, src, ' '.join(msg))
    elif msg[0] in commands:
        await commands[msg.pop(0)](self, c, src, ' '.join(msg))


admin_commands = {
    'cheat': cheat,
    'purge': purge
}

commands = {
    'eat': eat,
    'recipe': recipe,
    'bake': bake,
    'bakeall': bakeall,
    'inv': invsee,
    'items': invsee,
    'goods': invsee,
    'give': give,
    'giveall': giveall,
    'richest': richest,
    'info': info,
    'owners': owners
}


async def init(self):
    self.handle_cmd['ov'] = ov_handle
    self.handle_raw['oven'] = generate

    self.help['ov'] = ['ov <command> - a worthless ripoff of badger by lickthecheese and Yours Truly', 'ov subcommands: info bake cheat items|inv|goods purge give giveall owners richest']
    self.help['ov info'] = ['info <item> - get info for item']
    self.help['ov bake'] = ['bake <item> - bake some stuff']
    self.help['ov cheat'] = ['cheat <user> <item> - you are bad if you use it']
    self.help['ov items'] = ['items|inv|goods [user] - show the stuff in your inventory']
    self.help['ov inv'] = self.help['ov items']
    self.help['ov goods'] = self.help['ov items']

    self.help['ov purge'] = ['purge <user> - clear someone\'s inventory']
    self.help['ov give'] = ['give <user> <item> - give someone something from your inventory']
    self.help['ov giveall'] = ['giveall <user> <item> - give someone all of an item from your inventory']
    self.help['ov owners'] = ['owners <item> - see which users own an item']
    self.help['ov richest'] = ['richest [item] - see which users own the most valuable items']
