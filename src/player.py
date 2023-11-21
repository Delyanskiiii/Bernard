import youtube_dl
import discord

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

class Player():
    
    def __init__(self):
      self.playing = False

    def play(self, voice, command):
        print(command)
        if command == 'crazy':
          try:
            voice.play(discord.FFmpegPCMAudio(executable="C:/ffmpeg/ffmpeg.exe", source="../voice/fipo/crazy.mp3"))
          except Exception as e:
             print(e)
        elif command == 'octane' or command == 'high-octane':
          try:
            voice.play(discord.FFmpegPCMAudio(executable="C:/ffmpeg/ffmpeg.exe", source="../voice/system/murder.mp3"))
          except:
            pass
        elif command == 'mother':
          try:
            voice.play(discord.FFmpegPCMAudio(executable="C:/ffmpeg/ffmpeg.exe", source="../voice/system/steel.mp3"))
          except:
            pass
        elif command == 'sigma':
          try:
            voice.play(discord.FFmpegPCMAudio(executable="C:/ffmpeg/ffmpeg.exe", source="../voice/system/sigma.mp3"))
          except:
            pass
        else:
           pass
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