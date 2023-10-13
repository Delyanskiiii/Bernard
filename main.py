import sys

sys.dont_write_bytecode = True
# from dis import disco
# import discord
# import numpy as np
# import soundfile as sf
# import wavio as wv
# from os import path, remove
# import speech_recognition as sr
# import wave
# import pyttsx3
# from discord.ext import commands
# from discord.utils import get
# intents = discord.Intents.default()
# intents.message_content = True
# client = commands.Bot(intents = intents, command_prefix = '.')
from bot_token import YOUR_BOT_TOKEN_HERE

# converter = pyttsx3.init()
# r = sr.Recognizer()
# # mic = sr.Microphone()
# voices = converter.getProperty('voices')
# converter.setProperty('rate', 200)
# converter.setProperty('volume', 0.9)
# converter.setProperty('voice', 'HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_EN-US_DAVID_11.0')
# freq = 44100
# recording_sink = discord.sinks.WaveSink()
# current_command = ""

# language = 'en-uk'
# players = {}

# boss = 498186376567717888
# trusted = [498186376567717888, 402467955977355275, 149944973125615617]

import discord

bot = discord.Bot(debug_guilds=[...])

@bot.event
async def on_ready():
    print('We have logged in as {0.user}'.format(bot))

# @client.command()
# async def voice(ctx):
#     for voice in voices:
#     # to get the info. about various voices in our PC 
#         print("Voice:")
#         print("ID: %s" %voice.id)
#         print("Name: %s" %voice.name)
#         print("Age: %s" %voice.age)
#         print("Gender: %s" %voice.gender)
#         print("Languages Known: %s" %voice.languages)




# @client.command(pass_context = True)
# async def join(ctx):
#     channel = ctx.message.author.voice.channel
#     current_channel = await channel.connect()
#     # print(current_channel.endpoint)
#     print(ctx.voice_client.channel)

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

# @client.command(pass_context = True)
# async def leave(ctx):
#     await ctx.guild.voice_client.disconnect()

# @client.command(name="ping")
# async def ping(ctx: commands.Context):
#     await ctx.send(f"Pong! {round(client.latency * 1000)}ms")

# @client.command()
# async def record(ctx):
#     ctx.voice_client.start_recording(discord.sinks.WaveSink(), finished_callback, ctx)

# @client.command()
# async def fipo(ctx):
#     voice = await ctx.message.author.voice.channel.connect()
#     voice.play(discord.FFmpegPCMAudio(executable="C:/ffmpeg/ffmpeg.exe", source="C:/Bernard/recordings/fipo/crazy.mp3"))

# async def finished_callback(sink, ctx):

#     recorded_users = {
#         f"<@{user_id}>": audio
#         for user_id, audio in recording_sink.audio_data.items()
#     }

#     files = [discord.File(audio.file, f"{user_id}.{sink.encoding}") for user_id, audio in sink.audio_data.items()]

#     await ctx.channel.send(f"Finished! Recorded audio for {', '.join(recorded_users.keys())}.", files=files)

#     for f in files:
#                         #Reset the buffer seek position,
#                         # so that it reads from the start of the file
#         f.fp.seek(0)
#         data = f.fp
#                     #Open buffer 'File-like Object'
#                     # and write wav audio data to it
#         with wave.open(data, "wb") as f:
#             f.setnchannels(ctx.voice_client.decoder.CHANNELS)
#             f.setsampwidth(ctx.voice_client.decoder.SAMPLE_SIZE // ctx.voice_client.decoder.CHANNELS)
#             f.setframerate(ctx.voice_client.decoder.SAMPLING_RATE)
#                     #Reset buffer seek position again 
#                     # (not sure this is neccessary, but used for safety)
#         data.seek(0)
#         audio_buffer = data.read()
#         audio_array = np.frombuffer(audio_buffer, dtype=np.int32, count=-1)
#         sf.write("recording0.wav", audio_array, ctx.voice_client.decoder.SAMPLING_RATE)
#         with sr.AudioFile("C:/Bernard/recording0.wav") as source:
#             audio_data = r.record(source)
#             text = r.recognize_google(audio_data, language = 'bg-BG', show_all = True)
#             print(text)
#             current_command = text
#             await ctx.channel.send(text)
    

# @client.command()
# async def stop_recording(ctx):
#     ctx.voice_client.stop_recording()


# @client.command()
# async def play(ctx, url):
#     server = ctx.message.guild
#     voice_client = ctx.message.author.voice.channel
#     player = await voice_client.create_ytdl_player(url)
#     players[server.id] = player
#     player.start()


# @client.event
# async def on_voice_state_update(member, before, after):
#     user = member.id
#     voice_client = discord.utils.get(client.voice_clients, guild = member.guild)

#     '''
#     try:
#         if after.requested_to_speak_at() is not None:
#             print("gospod bog")
#     except:
#         print("ne e gospod")
#     #if before.requested_to_speak_at() is not after.requested_to_speak_at():
#         #print("gospod bog")
#     voice_manager = discord.GetVoiceManager()
#     inputMode = voice_manager.GetInputMode()
#     if inputMode.Type == 1:
#         print("da, gospod e")
#         '''

#     if user == boss:
#         if after.channel is not None:
#             if before.channel is None:
#                 await after.channel.connect()
#             elif before.channel is not after.channel and voice_client is not None:
#                 await member.guild.voice_client.move_to(after.channel)
#             elif before.channel is not after.channel and voice_client is None:
#                 await after.channel.connect()

bot.run(YOUR_BOT_TOKEN_HERE)