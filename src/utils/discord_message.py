def chunks(queue: list) -> list:
    chunks = []
    chunk_size = 15
    for index in range(0, len(queue), chunk_size):
        start_index = index
        end_index = index + chunk_size
        chunk = []
        for i in range(start_index, min(end_index, len(queue))):
            chunk.append(queue[i])
        chunks.append(chunk)
    return chunks

def formatted(queue, start_index):
    message = ''
    for index, item in enumerate(queue, start=start_index):
        message += f'{index}. {item.title} - {item.webpage_url}\n'
    return f'```{message}```'