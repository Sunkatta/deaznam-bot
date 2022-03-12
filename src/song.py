from discord import FFmpegAudio


class Song:
    def __init__(self, title: str, webpage_url: str, player: FFmpegAudio):
        self.title = title
        self.webpage_url = webpage_url
        self.player = player
