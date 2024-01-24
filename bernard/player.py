import discord
import yt_dlp

class Player():
    '''Represents audio player once in voice channel.
    Handles all the requests from the users.
    '''
    def __init__(self, voice):
        self.voice = voice
        self.audio = None
        self.queue = []
        self.volume = 10
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

    def play_next(self):
        self.skip()
        print(self.queue)
        if len(self.queue) > 0:
            self.play(self.queue[0])
            self.queue.pop(0)

    def play(self, audio):
        if not self.audio and audio != '':
            try:
                with yt_dlp.YoutubeDL(self.ydl_opts) as ydl:
                    info = ydl.extract_info(f"ytsearch:{audio}", download=False)
                    url = info['entries'][0]['url']
                
                self.audio = discord.FFmpegPCMAudio(url, **self.FFMPEG_OPTIONS)
                self.voice.play(self.audio, after=lambda e: self.play_next())
                self.set_volume(self.volume)
            except Exception as e:
                print(e)

        else:
            self.queue.append(audio)

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

    def clear_queue(self):
        self.queue = []

    def set_volume(self, volume):
        if self.audio:
            print(volume/100)
            self.voice.source = discord.PCMVolumeTransformer(self.voice.source, volume=volume/100)