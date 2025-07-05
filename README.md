# Deaznam Bot
A Discord bot whose main goal is to be integrated with a few music providers' APIs. More features might be added later.

# Installation
1. To install the required dependencies, please go to `cd src` and run `cd pip install --upgrade -r requirements.txt`.
2. You also need FFmpeg, e.g. by reaching https://www.gyan.dev/ffmpeg/builds/
3. Download `ffmpeg-git-full.7z` archive
4. Then extract it and put in your main disk folder with the name `FFmpeg`
5. Add it in paths' shortcuts as a new record in 'PATH' with the content: `<disk>:\FFmpeg\bin`
6. Add your env var for `BOT_AUTH_TOKEN`

Finally, to run the bot, a Bot Auth Token is required, which can be obtained from the Discord Developer Portal. For more information on how to get started with the Discord Developer Portal, please visit: [Creating a Bot Account](https://discordpy.readthedocs.io/en/stable/discord.html)

# Running the bot
The bot can be run either from the terminal or in your favorite IDE (e.g. VS Code):

`python main.py`

This default command will run the local bot instance using the default `.env` file. You can use a command argument to specify a different `.env` file, which can run a different bot instance. E.g., to use the `.env.example` file:

`python main.py --env example`