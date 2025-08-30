from models.song import Song

CHUNK_SIZE = 15
TEXT_SIZE = 77
EXAMPLE_URL_LENGTH = 43
SEPERATOR = ' - '
LEFT_ANGLE = '<'
RIGHT_ANGLE = '>'
ELLIPSIS = '...'
NEW_LINE = '\n'
MAX_MESSAGE_SIZE = ((len('10. ') + TEXT_SIZE + len(ELLIPSIS) + len(SEPERATOR) + len(
    LEFT_ANGLE) + EXAMPLE_URL_LENGTH + len(RIGHT_ANGLE) + len(NEW_LINE)) * CHUNK_SIZE)  # 1995


def chunks(queue: list[Song]) -> list[Song]:
    chunks = []
    for index in range(0, len(queue), CHUNK_SIZE):
        start_index = index
        end_index = index + CHUNK_SIZE
        chunk = []
        for i in range(start_index, min(end_index, len(queue))):
            chunk.append(queue[i])
        chunks.append(chunk)
    return chunks


def formatted(queue: list[Song], start_index: int) -> str:
    message = ''
    for index, item in enumerate(queue, start=start_index):
        message += f'{index}. {full_text(item)}{NEW_LINE}'
    return f'{message}'


def full_text(item: Song) -> str:
    title = __sliced_text(item.title)
    return f'{title}{SEPERATOR}{LEFT_ANGLE}{item.webpage_url}{RIGHT_ANGLE}'


def __sliced_text(text: str) -> str:
    return text[:TEXT_SIZE] + (ELLIPSIS if len(text) > TEXT_SIZE else '')
