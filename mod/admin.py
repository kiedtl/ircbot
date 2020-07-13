import config
import common, importlib, out, os, time

modname = 'admin'

async def quit(self, chan, source, msg):
    await self.quit()

async def restart(self, chan, source, msg):
    await self.quit()
    os.system('systemctl --user restart bot')

async def reloadmods(self, chan, source, msg):
    before = time.time()
    await out.msg(self, modname, chan,
        ['reloading modules...'])

    oldcmd  = self.handle_cmd
    oldraw  = self.handle_raw
    oldhelp = self.help

    self.handle_cmd = {}
    self.handle_raw = {}
    self.help = {}

    try:
        for i in self.modules:
            importlib.reload(self.modules[i])
            await self.modules[i].init(self)
    except Exception as e:
        await out.msg(self, modname, chan,
            [f'segmentation fault', repr(e)])
        self.handle_cmd = oldcmd
        self.handle_raw = oldraw
        self.help = oldhelp
        return

    await out.msg(self, modname, chan,
        ['{} modules reloaded in {}s'.format(len(self.modules),
            round(time.time() - before, 3))])

async def part(self, chan, source, msg):
    await self.part(msg)

async def join(self, chan, source, msg):
    await self.join(msg)

async def joins(self, chan, source, msg):
    for i in config.prod_chans:
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
    try:
        result = await aexec(self, ' '.join(msg))
    except Exception as e:
        await out.msg(self, modname, chan,
            [f'segmentation fault: {repr(e)}'])
    await out.msg(self, modname, chan,
        [f'result: \'{result}\''])

async def send(self, c, n, m):
    msg = m.split(' ')
    await self.message(msg.pop(0), ' '.join(msg))

async def shutup(self, c, n, m):
    duration = 5
    if len(m) >= 1:
        try:
            duration = int(m) + 0
        except:
            duration = 5
    self.asleep[c] = time.time() + (duration * 60)
    await out.msg(self, modname, chan,
        [f'disabled for {duration}m'])

async def wake(self, c, n, m):
    self.asleep[c] = time.time()
    await out.msg(self, modname, chan, ['I\'m back!'])

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
            await out.msg(self, modname, chan,
                [self.err_invalid_command])
            return
        print('{} recieved {} signal from {}'
            .format(common.modname('admin'), msg[0], source))
        await commands[msg.pop(0)](self, chan, source, ' '.join(msg))
    else:
        await out.msg(self, modname, chan,
            ['insufficient privileges'])

async def init(self):
    self.handle_cmd['admin'] = adminHandle
    self.handle_cmd['a'] = self.handle_cmd['admin']

    self.help['admin'] = ['admin - various bot owner commands',
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
