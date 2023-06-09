from cogs.music.song import Song

CHUNK_SIZE = 15
TEXT_SIZE = 78
EXAMPLE_URL_LENGTH = 43
SEPERATOR = ' - '
DELIMITER = '```'
ELLIPSIS = '...'
NEW_LINE = '\n'
MAX_MESSAGE_SIZE = len(DELIMITER) + ((len('10. ') + TEXT_SIZE + len(ELLIPSIS) + len(SEPERATOR) + EXAMPLE_URL_LENGTH + len(NEW_LINE)) * CHUNK_SIZE) + len(DELIMITER) # 1986

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
        message += f'{index}. {full_text(item)}{NEW_LINE}'
    return f'{DELIMITER}{message}{DELIMITER}'

def full_text(item: Song) -> str:
    title = __sliced_text(item.title)
    return f'{title}{SEPERATOR}{item.webpage_url}'

def __sliced_text(text: str) -> str:
    return text[:TEXT_SIZE] + (ELLIPSIS if len(text) > TEXT_SIZE else '')