class Song:
    def __init__(self, title: str, webpage_url: str, url: str):
        """
        :param title: Song title
        :param webpage_url: The URL used for display
        :param url: The song URL used for playback. Usually it is different from webpage_url
        """
        self.title = title
        self.webpage_url = webpage_url
        self.url = url
