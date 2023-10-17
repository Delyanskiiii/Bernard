import sys
sys.dont_write_bytecode = True
import discord
import asyncio
import select

import wave
import numpy as np
import soundfile as sf
import speech_recognition as sr
r = sr.Recognizer()

from discord.ext import commands
from tokens import YOUR_BOT_TOKEN, BOSS_ID

intents = discord.Intents.default()
intents.message_content = True
intents.voice_states = True
intents.members = True
client = commands.Bot(intents = intents, command_prefix = '.')


async def finished_callback(sink):
    print('callback')
    files = [discord.File(audio.file, f"{user_id}.{sink.encoding}") for user_id, audio in sink.audio_data.items()]

    for f in files:
        f.fp.seek(0)
        data = f.fp

        with wave.open(data, "wb") as f:
            f.setnchannels(client.voice_clients[0].decoder.CHANNELS)
            f.setsampwidth(client.voice_clients[0].decoder.SAMPLE_SIZE // client.voice_clients[0].decoder.CHANNELS)
            f.setframerate(client.voice_clients[0].decoder.SAMPLING_RATE)

        data.seek(0)
        audio_buffer = data.read()
        audio_array = np.frombuffer(audio_buffer, dtype=np.int32, count=-1)
        sf.write("recording.wav", audio_array, client.voice_clients[0].decoder.SAMPLING_RATE)

        with sr.AudioFile("./recording.wav") as source:
            audio_data = r.record(source)
            text = r.recognize_google(audio_data, language = 'bg-BG', show_all = True)
            if text != []:
                print(text)
                for trans in text['alternative']:
                    if trans['transcript'] == 'crazy':
                        client.voice_clients[0].play(discord.FFmpegPCMAudio(executable="C:/ffmpeg/ffmpeg.exe", source="./voice/fipo/crazy.mp3"))


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

    for guild in client.guilds:
        member = guild.get_member(BOSS_ID)
        if member and member.voice:
            voice = await member.voice.channel.connect()

    recording = False
    counter = 0
    while voice.is_connected():
        try:
            socket_len = len(voice.socket.recv(4096))

        except:
            socket_len = 43
            await asyncio.sleep(0.1)

        if socket_len <= 52:
            counter += 1
        else:
            counter = 0

        print(socket_len)
        if socket_len > 52 and not recording:# and len(voice.socket.recv(4096)) > 52:
            print('record')
            voice.start_recording(discord.sinks.WaveSink(), finished_callback)
            recording = True

        elif counter > 2 and recording:
            print('stop')
            voice.stop_recording()
            await asyncio.sleep(0.05)
            recording = False


@client.event
async def on_voice_state_update(member, before, after):
    if member.id == BOSS_ID and before.channel is not after.channel:
        if client.voice_clients == [] and after.channel is not None:
            await after.channel.connect()
        elif client.voice_clients != []:
            await client.voice_clients[0].move_to(after.channel)
    # elif member.id == BOT_ID and before.channel is not after.channel:
    #     if client.voice_clients == []:
    #         await before.channel.connect()
    #     else:
    #         await client.voice_clients[0].move_to(before.channel)

client.run(YOUR_BOT_TOKEN)