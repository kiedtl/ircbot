import importlib, time

async def quit(self, chan, source, msg):
    await self.quit('[ADMIN] recieved {} signal from {}'
            .format(msg, source))

async def reloadmods(self, chan, source, msg):
    await self.message(chan, '[ADMIN] reloading modules...')
    self.cmd = {}
    self.raw = {}
    self.help = {}
    for i in self.modules:
        importlib.reload(self.modules[i])
        await self.modules[i].init(self)
    await self.message(chan, '[ADMIN] done')

async def part(self, chan, source, msg):
  await self.message(chan, '[ADMIN] leaving channel {}'.format(msg))
  await self.part(msg)

async def join(self, chan, source, msg):
  await self.message(chan, '[ADMIN] joining channel {}'.format(msg))
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
  await aexec(self, ' '.join(msg))
  await self.message(chan, 'ok')

async def send(self, c, n, m):
  msg = m.split(' ')
  await self.message(msg.pop(0), ' '.join(msg))
  await self.message(c, 'ok')

async def shut(self, c, n, m):
  self.qtime[c] = time.time()+(60*10)
  await self.message(c, 'Ok, il be back')

commands = {
  'quit': quit,
  'reload': reloadmods,
  'commit': commit,
  'part': part,
  'join': join,
  'eval': ev,
  'send': send,
  'joins': joins,
  'shut': shut
}

async def adminHandle(self, chan, source, msg):
  if await self.is_admin(source):
    msg = msg.split(' ')
    if len(msg) < 1 or not msg[0] in commands:
      await self.message(chan, '[ADMIN] invalid command')
      return
    print('[ADMIN] recieved {} signal from {}'.format(msg[0], source))
    await commands[msg.pop(0)](self, chan, source, ' '.join(msg))
  else:
    await self.message(chan, '[ADMIN] insufficient privileges')


async def init(self):
  self.cmd['admin'] = adminHandle
  self.joins = ["#chaos", "#lickthecheese", "#windowsloser", "#cminecraft", "#team", "#clubcraft", "#rscmakerspace", "#archlinux", "#one", "#starlanes", "#ipd", "#pinebox",'#hamradio']
  
  self.help['admin'] = ['admin - various bot owner commands (more for subcommands)', 'sub-commands of admin, for more info do help admin <command>: quit reload commit part join joins eval send']
  self.help['admin quit'] = ['admin quit <message> - make the bot disconnect','no']
  self.help['admin reload'] = ['admin reload - reload the modules and configs', 'nothing to see here']
  self.help['admin commit'] = ['admin commit <action> - oh no (more)', 'suggested with <3 by khux']
  self.help['admin part'] = ['admin part <channel> - leave a channel', ':o']
  self.help['admin join'] = ['admin join <channel> - make the bot join a channel','...']
  self.help['admin joins'] = ['admin joins - join more channels', 'dont reconnect to a bunch of chans when the bots crashing etc']
  self.help['admin eval'] = ['admin eval <command> - absolute power corrupts absolutely', 'lmao']
  self.help['admin send'] = ['admin send <channel> <message> - send a message', 'lmao']




