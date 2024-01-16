import discord
import yt_dlp
import asyncio

class Player():
    '''Represents audio player once in voice channel.
    Handles all the requests from the users.
    '''
    def __init__(self, voice):
        self.voice = voice
        self.audio = None
        self.queue = []
        # self.future = asyncio.Future()
        self.ydl_opts = {
            'format': 'bestaudio/best',
            'noplaylist': True,
            'simulate': True,
            'skip_download': True,
            'quiet': True,
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
        }
        self.FFMPEG_OPTIONS = {
            'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 
            'options': '-vn'
        }

    async def play_next(self, loop):
        print(self.queue)
        if len(self.queue) == 0:
            self.skip()
        else:
            await self.play(self.queue[0], loop)
            # self.future.set_result(None)
            self.queue.pop(0)

    async def play(self, audio, loop):
        if not self.audio:
            with yt_dlp.YoutubeDL(self.ydl_opts) as ydl:
                info = ydl.extract_info(f"ytsearch:{audio}", download=False)
                url = info['entries'][0]['url']

            audio = await discord.FFmpegOpusAudio.from_probe(url, **self.FFMPEG_OPTIONS)
            # future = asyncio.Future()
            self.audio = audio
            self.voice.play(self.audio, after=lambda e: asyncio.run_coroutine_threadsafe(self.play_next(loop), loop))
            # result = await future
            # if result:
            #     await self.play_next()
        else:
            print('append')
            self.queue.append(audio)
            print(self.queue)

    def pause(self):
        if self.audio:
            self.voice.pause()

    def resume(self):
        if self.audio:
            self.voice.resume()

    def skip(self):
        if self.audio:
            self.voice.stop()
            self.audio = None

    # def set_volume(self, volume):
    #     if self.audio:
    #         current_volume = max(0.0, min(1.0, volume))
    #         print(current_volume)
    #         self.voice.source.volume = current_volume
    #         self.voice.source = discord.PCMVolumeTransformer(self.voice.source, volume=1.0)