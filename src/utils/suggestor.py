from youtubesearchpython import VideosSearch

def get_urls(input: str, suggest: str, limit: int) -> list:
    results = __search(input, limit)
    if len(results) == 0:
        results = __search(suggest, limit)

    urls = []
    i = 0
    while i < len(results):
        urls.append(results[i]['link'])
        i = i + 1

    return urls

def __search(query: str, limit: int) -> list:
    search = VideosSearch(query, limit)
    return search.result()['result']

def get_suggestions(title_words: list, tags: list) -> str:
    if len(tags) > 0:
        similar_words = []
        title_words = [s.lower() for s in title_words]
        tags = [s.lower() for s in tags]

        for title_word in title_words:
            for tag in tags:
                if title_word in tag or tag in title_word:
                    similar_words.append(tag)
        if len(similar_words) > 0:
            return similar_words[0]
        else:
            return tags[0]
    else:
        return ' '.join(title_words[:2])