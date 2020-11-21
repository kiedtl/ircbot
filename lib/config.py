botmaster = "kiedtl"
email = ["kiedtl", "tilde.team"]
upstream = ["https://github.com/", "kiedtl", "/ircbot"]
description = "a multi-purpose bot"
rollcall_fmt = "I'm {nickname}! | owner: {owner} | source: {source} | contact: {email} | usage: try {prefix}help"

nickname = "sigsegv"
username = "kiedtl_bots"
realname = description
server = "localhost"
tls = False
tls_verify = False

join_on_invite = True
set_botmode = True

prefix = ":"
admins = ["kiedtl", "spacehare"]

bannedchans = ["#meta", "##jmw2020", "#communism", "#chaos"]

# channels that are joined only when the
# `:admin joins` command is issued
prod_chans = ["#team", "#lounge", "#xfnw"]

# channels that are joined initially
initial_chans = ["#bots", "#spacehare", "#sigsegv"]

quitmsg = "kill -11 $$"
