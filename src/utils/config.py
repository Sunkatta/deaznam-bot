import yt_dlp

ytdl_format_options = {
    'format': 'bestaudio/best',
    'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    # 'verbose': True, # uncomment for logs
    'default_search': 'auto',
    # bind to ipv4 since ipv6 addresses cause issues sometimes
    'source_address': '0.0.0.0'
}

ytdl = yt_dlp.YoutubeDL(ytdl_format_options)

ffmpeg_options = {
   'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
   'options': '-vn'
}