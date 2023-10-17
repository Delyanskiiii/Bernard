# # mic = sr.Microphone()
# recording_sink = discord.sinks.WaveSink()
# import numpy as np
# import wavio as wv
# from os import path, remove
# import pyttsx3
# from dis import disco
# from discord.utils import get


# @client.command(pass_context = True)
# async def read(ctx):
#     # subprocess.call(['ffmpeg', '-i', 'quote.mp3', 'quote.wav'])
#     quote = "quote.wav"
#     with sr.AudioFile(quote) as source:
#         # listen for the data (load audio to memory)
#         audio_data = r.record(source)
#         # print(type(audio_data))
#         # recognize (convert from speech to text)
#         text = r.recognize_google(audio_data, language = 'en-EN')
#         print(text)

# @client.command(name="ping")
# async def ping(ctx: commands.Context):
#     await ctx.send(f"Pong! {round(client.latency * 1000)}ms")


# @client.command()
# async def play(ctx, url):
#     server = ctx.message.guild
#     voice_client = ctx.message.author.voice.channel
#     player = await voice_client.create_ytdl_player(url)
#     players[server.id] = player
#     player.start()

# readable, _, _ = select.select([voice.socket], [], [], 0.1)