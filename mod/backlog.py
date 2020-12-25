# backlogger
# temporarily stores messages for other modules to access (such as
# :pig, :owo, and :mock) and logs them

from datetime import datetime

modname = "backlog"

async def backlogger(self, chan, src, msg):
    if chan not in self.backlog:
        self.backlog[chan] = []

    if chan not in self.logfiles:
        logpath = f"irc/{chan}.log"
        self.log(modname, f"opening logfile {logpath}")
        self.logfiles[chan] = open(logpath, "a")

    # store in logfile
    time = datetime.strftime(datetime.now(), "%d%m%y%H%M")
    self.logfiles[chan].write(f"{time} {src} {msg}\n")
    self.logfiles[chan].flush()

    if src == self.nickname:
        return

    # don't store in backlog if msg is a command
    if msg[: len(self.prefix)] == self.prefix:
        cmd = msg[len(self.prefix) :]
        cmd = cmd.split(" ")[0]
        if cmd in self.handle_cmd:
            return

    self.backlog[chan].append([src, msg])

    # flush backlog if its size exceeds 128
    if len(self.backlog[chan]) > 128:
        del self.backlog[chan][:-64]


async def init(self):
    self.backlog = {}
    self.logfiles = {}
    self.handle_raw["backlog"] = backlogger
