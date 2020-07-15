# helper functions to deal with
# handlers.
#

def register(self, modname, func):
    '''
    Parse a functions docstring and then
    register it as a {cmd, raw, regex} handler.
    Set helptext and aliases, too.
    '''

    # TODO: cleanup data parsing
    # separate lexing from parsing
    #
    # TODO: split this up into multiple
    # functions

    # has this function already been registered?
    if hasattr(func, 'registered'):
        return

    data = {}
    data['name']   = ''
    data['help']   = []
    data['args']   = ''
    data['func']   = func
    data['module'] = modname

    doc = func.__doc__ or False
    if not doc:
        return

    last_item = ''

    for line in doc.split('\n'):
        line = line.lstrip(' ')
        if len(line) < 1:
            continue
        elif line[0] == ':':
            key, _, value = line.partition(': ')
            key = key.lstrip(':')
            if key in data and type(data[key]) is list:
                data[key].append(value)
            else:
                data[key] = value
            last_item = key
        elif line[0] == '>':
            if last_item == '':
                continue
            strpd = line.lstrip('>').lstrip(' ')
            if type(data[last_item]) is list:
                data[last_item][-1] += ' ' + strpd
            elif type(data[last_item]) is str:
                data[last_item] += strpd

    # parse arguments
    raw_args = data['args']
    data['args'] = []
    for raw_arg in raw_args.split():
        arg = {}

        # optional?
        if raw_arg[0] == '@':
            arg['optional'] = True
            raw_arg = raw_arg.lstrip('@')
        else:
            arg['optional'] = False

        name, _, _type = raw_arg.partition(':')
        arg['name'] = name
        arg['type'] = _type

        data['args'].append(arg)

    # format help string with name and args
    help_string = data['name'] + ' '
    for arg in data['args']:
        if arg['optional']:
            help_string += f'[{arg["name"]}] '
        else:
            help_string += f'<{arg["name"]}> '
    help_string += '- ' + data['help'][0]

    # register help messages
    self.help[data['name']] = [help_string] + data['help'][1:]

    # register aliases
    if 'aliases' in data:
        self.aliases[data['name']] = [al
            for al in data['aliases'].split()]

    # register handlers
    if 'hook' in data:
        if data['hook'] == 'cmd':
            self.handle_cmd[data['name']] = func
        elif data['hook'] == 'raw':
            self.handle_raw[data['name']] = func
        elif data['hook'] == 'reg':
            reg = re.compile(data['hook_regex'])
            self.handle_reg[data['name']] = (reg, func)

    func.registered = True
    return
