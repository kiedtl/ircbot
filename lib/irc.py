# some utility functions for outputting
# information

from __main__ import bot
import common

# cache output, module name
# on a per-channel basis
buf = {}
last_modname = {}

async def msg(mod, chan, msg):
    # TODO: throttling
    # (if the messages are too big)
    if chan in buf:
        del buf[chan]
    buf[chan] = msg[:] # copy list
    last_modname[chan] = mod

    fmt = '{}'
    if len(last_modname[chan]) > 1:
        fmt = common.modname(last_modname[chan]) + ' ' + fmt
    if len(buf[chan]) > 1:
        fmt = fmt + ' (more)'

    await bot.message(chan, fmt.format(buf[chan].pop(0)))

async def more(chan):
    if len(buf[chan]) == 0:
        await bot.message(chan, '{} no more text to show'
            .format(common.modname('more')))
        return

    fmt = '{}'
    if len(last_modname[chan]) > 1:
        fmt = common.modname(last_modname[chan]) + ' ' + fmt
    if len(buf[chan]) > 1:
        fmt = fmt + ' (more)'

    await bot.message(chan, fmt.format(buf[chan].pop(0)))
