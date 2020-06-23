async def init(self):
    # channels that are joined only when the
    # `:admin joins` command is issued
    self.joins = ['#team', '#lickthecheese', '#chaos',
        '#unruly']

    # channels that are joined initially
    self.chansjoin = ['#bots', '#spacehare']
