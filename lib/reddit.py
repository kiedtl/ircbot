# reddit stuff
# REQUIRE lib requests

import datetime
import fmt
import nullptr
import requests

PUSHSHIFT = 'https://api.pushshift.io/reddit/search/submission/'

def search_by_id(rd_id, subreddit=''):
    data = requests.get(f'{PUSHSHIFT}?ids={rd_id}&sort_type=score')
    return sorted(data.json()['data'],
        key=lambda x: x['score'], reverse=True)

def search_by_keywords(terms, subreddit=''):
    data = requests.get(f'{PUSHSHIFT}?title={terms}&sort_type=score')
    return sorted(data.json()['data'],
        key=lambda x: x['score'], reverse=True)

def search_by_url(url, subreddit=''):
    data = requests.get(f'{PUSHSHIFT}?url={url}&sort_type=score')
    return sorted(data.json()['data'],
        key=lambda x: x['score'], reverse=True)


def fmt_post_info(post):
    '''
    format post information into string.
    '''
    title = fmt.bold(post['title'])
    author = 'u/' + post['author']
    subreddit = 'r/' + post['subreddit']
    karma = fmt.green(str(post['score']) + '↑')
    comments = post['num_comments']

    date = int(post['created_utc'])
    date = datetime.datetime.fromtimestamp(date)
    date = datetime.datetime.strftime(date, '%Y-%M-%d')

    rd_id = post['id']
    rd_url = fmt.underline(f'https://redd.it/{rd_id}')

    main = f'{title} ({karma}) by {author} on {subreddit} uploaded on {date}'

    if post['full_link'] == post['url']:
        return main + f' ({rd_url})'
    else:
        try:
            link = nullptr.shorten(post['url'])
            link = fmt.underline(link)
        except:
            link = fmt.underline(post['url'])

        return main + f' ({rd_url} -> {link})'

