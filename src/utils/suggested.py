from youtubesearchpython import VideosSearch

def urls(input: str, suggest: str, limit: int) -> list:
    if not limit:
        limit = 1

    results = __search(input, limit)
    if not results:
        results = __search(suggest, limit)

    urls = []

    i = 0
    while i < len(results):
        urls.append(results[i]['link'])
        i = i + 1

    return urls

def __search(query, limit):
    search = VideosSearch(query, limit)
    return search.result()['result']

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