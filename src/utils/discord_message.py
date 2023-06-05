from cogs.music.song import Song
from youtubesearchpython import Comments

CHUNK_SIZE = 10
TEXT_SIZE = 92
# Max message size: ((2 + 3 + 3) + (92 * 2) + (2 * 3)) * 10 = 1980

def chunks(queue: list) -> list:
    chunks = []
    for index in range(0, len(queue), CHUNK_SIZE):
        start_index = index
        end_index = index + CHUNK_SIZE
        chunk = []
        for i in range(start_index, min(end_index, len(queue))):
            chunk.append(queue[i])
        chunks.append(chunk)
    return chunks

def formatted(queue: list, start_index: int) -> str:
    message = ''
    for index, item in enumerate(queue, start=start_index):
        message += f'{index}. {full_text(item)}\n'
    return f'```{message}```'

def full_text(item: Song) -> str:
    title = __comment_text(item.title)
    try:
        first_comment = Comments.get(item.webpage_url)['result'][0]
        content = __comment_text(first_comment['content'])
        likes = first_comment['votes']['simpleText'] + ' 👍'
    except:
        content = 'No comment'
        likes = 'Failed'
    return f'{title} > {content} < {likes}'

def __comment_text(text: str) -> str:
    return text[:TEXT_SIZE] + ('...' if len(text) > TEXT_SIZE else '')