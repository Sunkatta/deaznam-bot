import asyncio
from queue import Queue
from models.music_player import MusicPlayer
from models.song import Song
from utils import capture_ffmpeg, suggestor
from utils.config import ytdl


class MusicService:
    def __init__(self) -> None:
        self.music_players: dict[str, MusicPlayer] = {}

    def add_music_player(self, music_player_id: str) -> None:
        if music_player_id not in self.music_players:
            self.music_players[music_player_id] = MusicPlayer(music_player_id)

    def get_music_player_by_id(self, music_player_id: str) -> MusicPlayer:
        if music_player_id not in self.music_players:
            raise KeyError(f"Music player with id {music_player_id} not found")

        return self.music_players[music_player_id]

    def get_song_queue_by_music_player_id(self, music_player_id: str) -> Queue[Song]:
        if music_player_id not in self.music_players:
            return None

        return self.music_players[music_player_id].get_songs_in_queue()

    def remove_music_player_by_id(self, music_player_id: str) -> None:
        if music_player_id not in self.music_players:
            return

        self.music_players[music_player_id].clear_queue()
        self.music_players.pop(music_player_id)

    def skip_song(self, music_player_id: str) -> None:
        if music_player_id not in self.music_players:
            raise KeyError(f"Music player with id {music_player_id} not found")

        music_player = self.music_players[music_player_id]
        music_player.get_next_song()

    async def play(self, music_player_id: str, input: str, limit: int = 1) -> tuple[Queue[Song], list[Song]]:
        if music_player_id not in self.music_players:
            self.add_music_player(music_player_id)

        music_player = self.music_players[music_player_id]

        entries_info = await self.__prep_entries(input)
        songs_to_enqueue = entries_info['songs_to_enqueue']

        if limit > 1:
            urls = suggestor.get_urls(
                input, entries_info['suggest'], limit)
            for url in urls:
                if entries_info['url'] == url:
                    continue
                suggest_entries_info = await self.__prep_entries(url)
                songs_to_enqueue.extend(
                    suggest_entries_info['songs_to_enqueue'])

        music_player.add_songs(songs_to_enqueue)

        return (music_player.get_songs_in_queue(), songs_to_enqueue)

    async def __prep_entries(self, input: str) -> list:
        loop = asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(input, download=False))
        songs_to_enqueue = []
        if 'entries' in data:
            for entry in data['entries']:
                if entry is not None:
                    prep_entry = self.__prep_entry(entry)
                    songs_to_enqueue.append(prep_entry['song'])
        else:
            prep_entry = self.__prep_entry(data)
            songs_to_enqueue.append(prep_entry['song'])

        songs = {'songs_to_enqueue': songs_to_enqueue}
        return {**songs, **prep_entry['latest_info']}

    def __prep_entry(self, entry: dict) -> dict:
        capture_ffmpeg.capture(entry['url'])

        song = Song(entry['title'],
                    entry['webpage_url'],
                    entry['url'])

        suggest = suggestor.get_suggestions(
            entry['title'].split(' '), entry['tags'])
        return {
            'song': song,
            'latest_info': {'url': entry['webpage_url'], 'suggest': suggest}
        }
