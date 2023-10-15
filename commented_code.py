
# r = sr.Recognizer()
# # mic = sr.Microphone()
# recording_sink = discord.sinks.WaveSink()
# import numpy as np
# import soundfile as sf
# import wavio as wv
# from os import path, remove
# import speech_recognition as sr
# import wave
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
# async def record(ctx):
#     ctx.voice_client.start_recording(discord.sinks.WaveSink(), finished_callback, ctx)

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