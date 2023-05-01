from youtubesearchpython import VideosSearch
import urllib.parse

VIDEO_LIMIT = 10

def get(title: str) -> list:
    query = urllib.parse.quote(title)
    search = VideosSearch(query, limit=VIDEO_LIMIT)
    results = search.result()['result']

    urls = []

    i = 0
    while i < VIDEO_LIMIT:
        urls.append(results[i]['link'])
        i = i + 1

    return urls