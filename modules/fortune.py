import subprocess
from subprocess import Popen, PIPE, STDOUT

async def fortune(self, c, n, m):
    proc = Popen(["fortune"],
            stdout=PIPE, stderr=STDOUT)
    (out, err) = proc.communicate()
    exit = proc.wait()
    fort = out.decode('utf-8')
    await self.message(c, fort)

async def init(self):
    self.cmd['fortune'] = fortune
    self.help['fortune'] = ['fortune - get a fortune', '']