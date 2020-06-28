import dataset, out, random

modname = 'ducc'

async def ducc_update(self, c, n, m):
    """ update the duccs state """
    pass

async def ducc_cure(self, c, n, m):
    """ cure the ducc (need admin privs) """
    last_state = list(self.ducc_state.find())[-1]
    self.ducc_state.insert(
        dict(last_fed=last_state['last_fed'],
            health=100, stress=0, alive=True))

async def ducc_feed(self, c, n, m):
    """ feed the ducc and increase its health points """
    pass

async def ducc_pet(self, c, n, m):
    """ pet the ducc and decrease its stress level """
    pass

async def ducc_quack(self, c, n, m):
    """ QUACK! """
    quacks = ['~quack~', 'QUACK!']
    duccs  = ['\_o<', '\_O<', '(">', '("=']

    ducc = f'{random.choice(duccs)} {random.choice(quacks)}'
    await out.msg(self, modname, c, [ducc])

async def ducc_shoot(self, c, n, m):
    """ try to kill the ducc :( """
    pass

async def ducc_info(self, c, n, m):
    """ display health, stress, etc """
    pass

commands = {
    'cure':       ducc_cure,
    'feed':       ducc_feed,
    'pet':        ducc_pet,
    'quack':      ducc_quack,
    'shoot':      ducc_shoot,
    'info':       ducc_info
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
