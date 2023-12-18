import discord
import yt_dlp
from yt_dlp import YoutubeDL
from youtubesearchpython import VideosSearch
import logging

class Player():
    '''Represents audio player once in voice channel.
    Handles all the requests from the users.
    '''
    def __init__(self, voice):
        self.voice = voice
        self.audio = None
        self.queue = []
        yt_dlp_logger = logging.getLogger('yt_dlp')
        yt_dlp_logger.setLevel(logging.WARNING)
        self.YDL_OPTIONS = {'format': 'bestaudio/best'}
        self.FFMPEG_OPTIONS = {'options': '-vn'}

        self.vc = None
        self.ytdl = YoutubeDL(self.YDL_OPTIONS)

    def play_next(self):
        if len(self.queue) == 0:
            self.audio = None
        else:
            self.play(self.queue[0])
            self.queue.pop(0)

    def search_yt(self, item):
        if item.startswith("https://"):
            title = self.ytdl.extract_info(item, download=False)["title"]
            return{'source':item, 'title':title}
        search = VideosSearch(item, limit=1)
        return{'source':search.result()["result"][0]["link"], 'title':search.result()["result"][0]["title"]}

    def play(self, audio):
        if not self.audio:
            ydl_opts = {
                'format': 'bestaudio/best',
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }],
            }
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(f"ytsearch:{audio}", download=False)
                url = info['entries'][0]['url']

            audio = discord.FFmpegPCMAudio(url)
            self.audio = audio
            self.voice.play(self.audio, after=lambda e: self.play_next())
        else:
            self.queue.append(audio)

    def stop(self):
        if self.audio:
            self.voice.stop()
            self.audio = None

    def pause(self):
        if self.audio:
            self.voice.pause()

    def resume(self):
        if self.audio:
            self.voice.resume()

    def skip(self):
        self.stop()
        self.play_next()

    def set_volume(self, volume):
        if self.audio:
            current_volume = max(0.0, min(1.0, volume))
            print(current_volume)
            self.voice.source.volume = current_volume
            self.voice.source = discord.PCMVolumeTransformer(self.voice.source, volume=1.0)