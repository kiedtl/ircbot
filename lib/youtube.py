# helper funcs to deal with YT

# REQUIRE lib isodate
# REQUIRE lib googleapiclient
# REQUIRE lib urllib

import isodate, urllib
import googleapiclient.discovery
import googleapiclient.errors

class InvalidURLException(Exception):
    """
    Is there already an exception like this?
    Don't think so...
    """
    pass

def authenticate(api_key):
    """
    Return an authenticated youtube instance.
    """
    return googleapiclient.discovery.build('youtube', 'v3',
        developerKey=api_key)

def id_from_url(rawurl):
    """
    Extract YT video ID from a URL.
    """
    url = urllib.parse.urlparse(rawurl)
    query = urllib.parse.parse_qs(url.query)

    # credits to BitBot's creator for the next 6 loc
    if url.hostname == "youtu.be" and url.path:
        return url.path[1:]
    elif url.path == "/watch" and "v" in query:
        return query["v"][0]
    elif url.path == "/playlist" and "list" in query:
        return query["list"][0]
    else:
        raise InvalidURLException('bad url')

def video_info(youtube, v_id):
    """
    Get information for a video from it's id.
    """
    request = youtube.videos().list(
        part='snippet,contentDetails,statistics',
        id=v_id,
        locale='en_US.UTF8'
    )

    video = (request.execute())['items'][0]

    title    = video['snippet']['title']
    uploaded = video['snippet']['publishedAt'].split('T')[0]
    views    = int(video['statistics']['viewCount'])
    likes    = int(video['statistics']['likeCount'])
    dislikes = int(video['statistics']['dislikeCount'])
    channel  = video['snippet']['channelTitle']
    duration = isodate.parse_duration(video['contentDetails']['duration'])

    return {
        'title': title,
        'uploaded_at': uploaded,
        'views': views,
        'likes': likes,
        'dislikes': dislikes,
        'channel': channel,
        'duration': duration
    }

def fmt_video_info(info):
    """
    Format video information.
    """
    dur = {}
    dur['hours'], rem = divmod(info['duration'].seconds, 3600)
    dur['minutes'], dur['seconds'] = divmod(rem, 60)

    durfmt = f'{dur["seconds"]}s'
    if dur['minutes'] > 0:
        durfmt = f'{dur["minutes"]}m ' + durfmt
    if dur['hours'] > 0:
        durfmt = f'{dur["hours"]}h ' + durfmt

    return f'{info["title"]} ({durfmt}) uploaded by {info["channel"]}' + \
        f' on {info["uploaded_at"]}, {info["views"]:,} views' + \
        f' ({info["likes"]:,}↑↓{info["dislikes"]:,})'
