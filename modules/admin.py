from common import modname
import importlib, time, os

async def quit(self, chan, source, msg):
    await self.quit('{} recieved {} signal from {}'
            .format(modname('admin'), msg, source))

async def restart(self, chan, source, msg):
    await self.quit('{} recieved {} signal from {}'
            .format(modname('admin'), msg, source))
    os.system('systemctl --user restart bot')

async def reloadmods(self, chan, source, msg):
    before = time.time()
    await self.message(chan, '{} reloading modules...'
        .format(modname('admin')))
    self.cmd = {}
    self.raw = {}
    self.help = {}
    for i in self.modules:
        importlib.reload(self.modules[i])
        await self.modules[i].init(self)
    await self.message(chan, '{} {} modules reloaded in {}s'
        .format(modname('admin'), len(self.modules),
            round(time.time() - before, 3)))

async def part(self, chan, source, msg):
    await self.part(msg)

async def join(self, chan, source, msg):
    await self.join(msg)

async def joins(self, chan, source, msg):
    for i in self.joins:
        await self.join(i)

async def aexec(self, code):
    # Make an async function with the code and `exec` it
    exec(
        f'async def __ex(self): ' +
        ''.join(f'\n {l}' for l in code.split('\n'))
    )

    # Get `__ex` from local variables, call it and return the result
    return await locals()['__ex'](self)

async def ev(self, chan, source, msg):
    msg = msg.split(' ')
    result = await aexec(self, ' '.join(msg))
    await self.message(chan, '{} result: \'{}\''
        .format(modname('admin'), result))

async def send(self, c, n, m):
    msg = m.split(' ')
    await self.message(msg.pop(0), ' '.join(msg))
    await self.message(c, 'ok')

async def shutup(self, c, n, m):
    duration = 5
    if len(m) >= 1:
        try:
            duration = int(m) + 0
        except:
            duration = 5
    self.asleep[c] = time.time() + (duration * 60)
    await self.message(c, '{} disabled for {}m'
        .format(modname('admin'), duration))

async def wake(self, c, n, m):
    self.asleep[c] = time.time()
    await self.message(c, '{} I\'m back!'
        .format(modname('admin')))

commands = {
    'quit': quit,
    'restart': restart,
    'reload': reloadmods,
    'part': part,
    'join': join,
    'eval': ev,
    'send': send,
    'joins': joins,
    'sleep': shutup,
    'wake': wake,
}

async def adminHandle(self, chan, source, msg):
    if await self.is_admin(source):
        msg = msg.split(' ')
        if len(msg) < 1 or not msg[0] in commands:
            await self.message(chan, '{} {}'
                .format(modname('admin'), self.err_invalid_command))
            return
        print('{} recieved {} signal from {}'
            .format(modname('admin'), msg[0], source))
        await commands[msg.pop(0)](self, chan, source, ' '.join(msg))
    else:
        await self.message(chan, '{} insufficient privileges'
            .format(modname('admin')))

async def init(self):
    self.cmd['admin'] = adminHandle
    self.cmd['a'] = self.cmd['admin']

    self.admins = ['kiedtl', 'segmentation', 'admin', 'glenda',
            'spacehare_',
            'spacehare', 'ben', 'cmccabe', 'gbmor', 'tomasino',
            'ubergeek', 'deepend', 'calamitous', 'khuxkm']

    self.help['admin'] = ['admin - various bot owner commands (more for subcommands)',
        'admin subcommands: quit restart reload part join joins eval send sleep wake']
    self.help['admin quit'] = ['admin quit <message> - shutdown bot']
    self.help['admin restart'] = ['admin restart <message> - restart bot']
    self.help['admin reload'] = ['admin reload - reload modules and configs']
    self.help['admin part'] = ['admin part <channel> - make bot leave channel']
    self.help['admin join'] = ['admin join <channel> -  make bot join channel']
    self.help['admin joins'] = ['admin joins - join channels defined in the admin module']
    self.help['admin eval'] = ['admin eval <command> - evaluate command']
    self.help['admin send'] = ['admin send <channel> <message> - send message']
    self.help['admin sleep'] = ['admin sleep [num] - send me into an enchanted sleep for [num] minutes (default: 5m)']
    self.help['admin wake'] = ['admin wake - wake me up from an enchanted sleep']
