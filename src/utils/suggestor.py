import traceback
from yt_dlp import YoutubeDL


def get_urls(input: str, suggest: str, limit: int) -> list:
    results = __search(input, limit)
    if len(results) == 0:
        results = __search(suggest, limit)
    return [result["link"] for result in results]


def __search(query: str, limit: int) -> list:
    try:
        options = {
            "quiet": True,
            "no_warnings": True,
        }

        with YoutubeDL(options) as ydl:
            result = ydl.extract_info(
                f"ytsearch{limit}:{query}",
                download=False,
            )

        return [
            {"link": entry["webpage_url"]}
            for entry in result.get("entries", [])
            if entry.get("webpage_url")
        ]
    except Exception as e:
        print(traceback.format_exc())
        return []


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
        return " ".join(title_words[:2])
