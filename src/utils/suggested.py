from youtubesearchpython import VideosSearch
import urllib.parse

LIMIT = 10

def get(title: str, limit: int) -> list:
    query = urllib.parse.quote(title)
    search = VideosSearch(query, limit=limit)
    results = search.result()['result']

    urls = []

    i = 0
    while i < limit:
        urls.append(results[i]['link'])
        i = i + 1

    return urls