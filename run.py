import discord
import numpy as np
import random
import wave
import asyncio
import soundfile as sf
from discord.ext import commands
import speech_recognition as sr

intents = discord.Intents.default()
intents.message_content = True
client = commands.Bot(intents = intents, command_prefix = '.') 
boss = 498186376567717888

TOKEN = 'OTQwNjMwMjcyNzQ2MDc4MjE4.YgKMNQ.ypgQzSK-Q1a8XEhIUtPXUsNl_CE'
r = sr.Recognizer()

@client.command()
async def record(ctx):
    ctx.voice_client.start_recording(discord.sinks.WaveSink(), finished_callback, ctx)

async def finished_callback(sink, ctx):
    global current_command

    files = [discord.File(audio.file, f"{user_id}.{sink.encoding}") for user_id, audio in sink.audio_data.items()]

    for f in files:
                        #Reset the buffer seek position,
                        # so that it reads from the start of the file
        f.fp.seek(0)
        data = f.fp
                    #Open buffer 'File-like Object'
                    # and write wav audio data to it
        with wave.open(data, "wb") as f:
            f.setnchannels(ctx.voice_client.decoder.CHANNELS)
            f.setsampwidth(ctx.voice_client.decoder.SAMPLE_SIZE // ctx.voice_client.decoder.CHANNELS)
            f.setframerate(ctx.voice_client.decoder.SAMPLING_RATE)
                    #Reset buffer seek position again 
                    # (not sure this is neccessary, but used for safety)
        data.seek(0)
        audio_buffer = data.read()
        audio_array = np.frombuffer(audio_buffer, dtype=np.int32, count=-1)
        sf.write("recording0.wav", audio_array, ctx.voice_client.decoder.SAMPLING_RATE)
        with sr.AudioFile("C:/Bernard/recordings/system/recording0.wav") as source:
            audio_data = r.record(source)
            text = r.recognize_google(audio_data, language = 'bg-BG', show_all = True)
            conversation(text, ctx)
    

@client.command()
async def stop_recording(ctx):
    ctx.voice_client.stop_recording()


async def conversation(user_input, ctx):
    await ctx.channel.send(user_input)




@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))




@client.command(pass_context = True)
async def join(ctx):
    channel = ctx.message.author.voice.channel
    await channel.connect()



@client.event
async def on_voice_state_update(member, before, after):
    user = member.id
    voice_client = discord.utils.get(client.voice_clients, guild = member.guild)

    if user == boss:
        if after.channel is not None:
            if before.channel is None:
                await after.channel.connect()
            elif before.channel is not after.channel and voice_client is not None:
                await member.guild.voice_client.move_to(after.channel)
            elif before.channel is not after.channel and voice_client is None:
                await after.channel.connect()

client.run(TOKEN)