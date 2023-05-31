from youtubesearchpython import VideosSearch
import urllib.parse

LIMIT = 1

def urls(input: str, limit: int) -> list:
    if not limit:
        limit = LIMIT
    query = urllib.parse.quote(input)
    search = VideosSearch(query, limit=limit)
    results = search.result()['result']

    if not results:
        return []

    urls = []

    i = 0
    while i < len(results):
        urls.append(results[i]['link'])
        i = i + 1

    return urls

def spicy_take(title_words: list, tags: list) -> str:
    if len(tags) > 0:
        similar_words = []
        for title_word in title_words:
            for tag in tags:
                if title_word.lower() in tag.lower() or tag.lower() in title_word.lower():
                    similar_words.append(tag)
        if len(similar_words) > 0:
            return similar_words[0]
        else:
            return tags[0]
    else:
        return ' '.join(title_words[:2])