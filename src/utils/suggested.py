from youtubesearchpython import VideosSearch
import urllib.parse

LIMIT = 1

def get(title: str, limit: int) -> list:
    if not limit:
        limit = LIMIT
    query = urllib.parse.quote(title)
    search = VideosSearch(query, limit=limit)
    results = search.result()['result']

    if not results:
        return []

    urls = []

    i = 0
    while i < limit:
        urls.append(results[i]['link'])
        i = i + 1

    return urls