from queue import Queue

from models.song import Song


class MusicPlayer:
    def __init__(self, id: str) -> None:
        self.id = id
        self.current_song: Song = None
        self.song_queue = Queue()

    def add_song(self, song: Song) -> None:
        if self.song_queue.qsize() == 0:
            self.current_song = song

        self.song_queue.put(song)

    def add_songs(self, songs: list[Song]) -> None:
        if self.song_queue.qsize() == 0:
            self.current_song = songs[0]

        list(map(self.song_queue.put, songs))

    def get_current_song(self) -> Song:
        return self.current_song

    def get_next_song(self) -> Song:
        self.current_song = self.song_queue.get()
        return self.current_song

    def get_songs_in_queue(self) -> Queue[Song]:
        return self.song_queue

    def clear_queue(self) -> None:
        self.current_song = None
        self.song_queue.queue.clear()
