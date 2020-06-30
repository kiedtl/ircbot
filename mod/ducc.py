import datetime, dataset, out, random
from datetime import timedelta
from babel.dates import format_timedelta

modname = 'ducc'

def ducc_hp_to_str(lvl):
    """ convert health points to string """
    hp_str = {
        # 0 == death
        7:   'dying',
        14:  'very ill',
        35:  'ill',
        42:  'neglected',
        70:  'alright',
        84:  'just fine',
        100: 'perfectly healthy',
    }

    while not lvl in hp_str:
        lvl -= 1
    return hp_str[lvl]

def ducc_sl_to_str(lvl):
    """ convert stress level to str """
    sl_str = {
        0: 'perfectly happy',
        7: 'happy',
        14: 'a little nervous',
        28: 'nervous',
        35: 'very nervous',
        48: 'a bit stressed',
        56: 'very stress out',
        70: 'alarmed',
        95: 'extremely stressed',
        # 100 == death
    }

    while not lvl in sl_str:
        lvl += 1
    return sl_str[lvl]

async def ducc_update(self, c, n, m):
    """ update the duccs state """
    pass

async def ducc_cure(self, c, n, m):
    """ cure the ducc (need admin privs) """
    last_state = list(self.ducc_state.find())[-1]
    self.ducc_state.insert(
        dict(last_fed=int(datetime.datetime.now().strftime('%s')),
            health=100, stress=0, alive=True))

async def ducc_feed(self, c, n, msg):
    """ feed the ducc and increase its health points """
    m = msg.split(' ')

    # check items
    for thing in m:
        if len(thing) < 1:
            await out.msg(self, modname, c, [f'you can\'t give air!'])
            return

        inv = self.ovendb['inv']
        its = inv.find_one(name=n, item=thing)

        if its == None:
            await out.msg(self, modname, c,
                [f'you don\'t have a {thing}! (see :ov inv)'])
            return
        if thing not in self.bakedGoods \
            or self.bakedGoods[thing] < 10 \
            or thing == 'ducc': # why would a ducc want to eat a ducc??
                await out.msg(self, modname, c,
                    [f'the ducc isn\'t interested in that...'])
                return

    # delete items
    for thing in m:
        inv.delete(id=its['id'])

    await out.msg(self, modname, c, [f'you fed the ducc!'])
    # TODO: increase health points

async def ducc_pet(self, c, n, m):
    """ pet the ducc and decrease its stress level """
    pass

async def ducc_quack(self, c, n, m):
    """ QUACK! """
    quacks = ['~quack~', 'QUACK!']
    duccs  = ['\_o<', '\_O<', '\_0<', '|\_( o)<']

    ducc = f'{random.choice(duccs)} {random.choice(quacks)}'
    await out.msg(self, modname, c, [ducc])

async def ducc_shoot(self, c, n, m):
    """ try to kill the ducc :( """
    pass

async def ducc_info(self, c, n, m):
    """ display health, stress, etc """
    state = list(self.ducc_state.find())[-1]

    alive = bool(state['alive'])
    health = ducc_hp_to_str(state['health'])
    stress = ducc_sl_to_str(state['stress'])

    last_fed_unix = int(state['last_fed'])
    last_fed_date = datetime.datetime.fromtimestamp(last_fed_unix)
    since = datetime.datetime.now() - last_fed_date
    since_delta_fmt = format_timedelta(since, locale='en_US')

    if not alive:
        await out.msg(self, modname, c, ['the ducc is dead!'])
        return

    await out.msg(self, modname, c,
        [f'the ducc is {health} and is feeling {stress}. It was last fed {since_delta_fmt} ago.'])

commands = {
    'cure':  ducc_cure,
    'feed':  ducc_feed,
    'pet':   ducc_pet,
    'quack': ducc_quack,
    'shoot': ducc_shoot,
    'info':  ducc_info
}

async def ducc_handle(self, c, src, msg):
    msg = msg.split(' ')
    if len(msg) < 1 or not msg[0] in commands:
        await out.msg(self, modname, c, [self.err_invalid_command])
        return
    await commands[msg.pop(0)](self, c, src, ' '.join(msg))

async def init(self):
    self.duccdb = dataset.connect('sqlite:///dat/ducc.db')
    self.ducc_state = self.duccdb['state']

    self.cmd['ducc'] = ducc_handle
    self.cmd['du']   = ducc_handle
