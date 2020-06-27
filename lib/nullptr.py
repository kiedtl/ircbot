# some helper functions to deal
# with 0x0.st-esque websites

import requests

def shorten(url, nullptr = 'https://0x0.st/'):
    params = { 'shorten': url }
    res = requests.post(url = nullptr, data = params)

    if res.status_code != 200:
        raise Exception(f'received {res.status_code}')

    url = res.text.rstrip()
    return url
