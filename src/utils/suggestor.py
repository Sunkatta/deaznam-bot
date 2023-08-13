from youtubesearchpython import VideosSearch

def get_urls(input: str, suggest: str, limit: int) -> list:
    results = __search(input, limit)
    if len(results) == 0:
        results = __search(suggest, limit)
    return [result['link'] for result in results]

def __search(query: str, limit: int) -> list:
    search = VideosSearch(query, limit)
    return search.result()['result']

def get_suggestions(title_words: list, tags: list) -> str:
    if len(tags) > 0:
        title_words = [s.lower() for s in title_words]
        tags = [s.lower() for s in tags]

        for title_word in title_words:
            for tag in tags:
                if title_word in tag or tag in title_word:
                    return tag
        return tags[0]
    else:
        return ' '.join(title_words[:2])