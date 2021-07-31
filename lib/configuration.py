# key-value storage system for the bot.
#
# tables:
#   #<chan>@<network>  ( key: string, value: string )
#    <user>@<network>  ( key: string, value: string )
#
# configuration values that are "exported" by modules
# can be configured on IRC by identified users and opers

import dataset

CONFIG_DB = dataset.connect("sqlite:///dat/config.db")


def get(network, ctx, key, default=None, cast=None):
    ch_table = CONFIG_DB[f"{ctx}@{network}"]
    row = ch_table.find_one(key=key)

    if not row:
        if default:
            ch_table.insert(dict(key=key, value=default))
        return try_cast(cast, default)
    else:
        return try_cast(cast, row["value"])


def set(network, ctx, key, value):
    ch_table = CONFIG_DB[f"{ctx}@{network}"]
    row = ch_table.find_one(key=key)

    if not row:
        ch_table.insert(dict(key=key, value=value))
    else:
        updated = dict(key=key, value=value)
        ch_table.update(updated, ["key"])


def try_cast(cast, value):
    if cast:
        if cast == bool and type(value) == str:
            value = value.lower() == "on" or \
                value.lower() == "yes" or \
                value.lower() == "true"
        else:
            value = cast(value)
    return value
