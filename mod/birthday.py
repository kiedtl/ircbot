import configuration
import datetime
import dateutil.parser
import manager
from manager import *

modname = "birthday"
VALID_DATE = r"(\d{4}-\d{2}-\d{2}|\d{2}-(jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec))"

@manager.hook(modname, "birthday", access=AccessType.IDENTIFIED)
@manager.argument("user", optional=True)
@manager.helptext(["see your (or someone else's) birthday"])
@manager.config("birthday", ConfigScope.USER, VALID_DATE, "YYYY-MM-DD or DD-MMM")
async def birthday(self, chan, nick, msg):
    user = self.users[nick]['account']
    birthday_str = configuration.get(self.network, user, "birthday")
    today = datetime.datetime.today()

    if not birthday_str:
        await self.msg(modname, chan, [f"no birthday set for {user}"])
        return

    try:
        birthday = dateutil.parser.parse(birthday_str)
    except:
        await self.msg(modname, chan, [f"invalid birthday '{birthday}' set for {user}"])
        return

    birthday_year = birthday.year
    birthday_date = birthday.replace(year=(today.year + 1))

    years = today.year - birthday_year
    days = birthday_date - today
    await self.msg(modname, chan, [f"{user} is {years + 1} in {days.days + 1} days"])


async def init(self):
    manager.register(self, birthday)
