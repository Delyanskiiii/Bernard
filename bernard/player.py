# import youtube_dl
import discord
# import discord

# async def shoa(client, query):
#     loop = client.loop
#     youtube_dl_opts = {
#         'format': 'bestaudio/best',
#         'postprocessors': [{
#             'key': 'FFmpegExtractAudio',
#             'preferredcodec': 'mp3',
#             'preferredquality': '192',
#         }],
#         'quiet': True,
#     }

#     with youtube_dl.YoutubeDL(youtube_dl_opts) as ydl:
#         info_dict = await loop.run_in_executor(None, lambda: ydl.extract_info(f'ytsearch:{query}', download=False))

#         if 'entries' in info_dict:
#             # Take the first result from the search
#             return info_dict['entries'][0]['url']

#     return None

# discord.FFmpegPCMAudio(executable="C:/ffmpeg/ffmpeg.exe", source="../voice/fipo/crazy.mp3")
class Player():
    
    def __init__(self, voice):
      self.voice = voice
      self.audio = None

    def reset_audio(self):
        print('reseting')
        self.audio = None
    
    def get_audio(self):
        print(self.audio)

    def play(self, audio):
        if not self.audio:
            self.audio = audio
            self.voice.play(self.audio, after=lambda e: self.reset_audio())

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

    def set_volume(self, volume):
        if self.audio:
            current_volume = max(0.0, min(1.0, volume))
            print(current_volume)
            self.voice.source.volume = current_volume
            self.voice.source = discord.PCMVolumeTransformer(self.voice.source, volume=1.0)
        # if not self.playing:
        #     ydl_opts = {
        #       'format': 'bestaudio',
        #       'postprocessors': [{
        #           'key': 'FFmpegExtractAudio',
        #           'preferredcodec': 'mp3',
        #           'preferredquality': '192',
        #       }],
        #     }

        #     with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        #         youtube_url = await shoa(client, url)

        #         if youtube_url:
        #             voice.play(discord.FFmpegPCMAudio(youtube_url), after=lambda e: print('done', e))

                # info = ydl.extract_info(url, download=False)
                # url2 = info['formats'][0]['url']

                # voice.play(discord.FFmpegPCMAudio(url2), after=lambda e: print('done', e))