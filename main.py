from dis import disco
from email.mime import audio
import discord
import asyncio
import json
from io import StringIO
import os
import subprocess
import wavio
from pydub import AudioSegment
import io
import scipy.io.wavfile
import numpy as np
import random
import struct
import base64
import ffmpeg
import soundfile as sf
import requests
import time
import file_operations
from scipy.io.wavfile import write
import wavio as wv
from os import path, remove
import speech_recognition as sr
import sys
import wave
import pyttsx3
import youtube_dl
from io import BytesIO
from gtts import gTTS
from discord.ext import commands
from scipy.io.wavfile import read, write
from discord.utils import get
# from rasterio.io import MemoryFile
intents = discord.Intents.default()
intents.message_content = True
client = commands.Bot(intents = intents, command_prefix = '.')                                                                         #Client prefix

TOKEN = 'OTQwNjMwMjcyNzQ2MDc4MjE4.YgKMNQ.ypgQzSK-Q1a8XEhIUtPXUsNl_CE'                                               #Token
converter = pyttsx3.init()
r = sr.Recognizer()
# mic = sr.Microphone()
voices = converter.getProperty('voices')
converter.setProperty('rate', 200)
converter.setProperty('volume', 0.9)
converter.setProperty('voice', 'HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_EN-US_DAVID_11.0')
freq = 44100
recording_sink = discord.sinks.WaveSink()
current_command = ""


rate = 22050  # samples per second
T = 3         # sample duration (seconds)
f = 440.0     # sound frequency (Hz)
t = np.linspace(0, T, T*rate, endpoint=False)
x = np.sin(2*np.pi * f * t)


language = 'en-uk'
players = {}

boss = 498186376567717888
trusted = [498186376567717888, 402467955977355275, 149944973125615617]                                              #Trusted list
sigmaQuotes = [
    'Yes I talk to myself because sometimes I need a professional opinion',
    'Do alcoholics run in your family? No, they drive.',
    'If she leaves you for another, Theres always her mother',
    'Violence is never the answer, it is the question, and the answer is yes.',
    'A true sigma can\'t die from a heart attack, but a heart can die from a sigma attack.',
    'Betas get laid, Sigmas get paid',
    'It\'s not "paranoid schizophrenia", it\'s Sigma male awareness.',
    'Don\'t destroy your goal just for a hole',
    'A foolish man complains about the hole in his pocket... A wise man uses that hole to scratch his balls...',
    'Don’t ever let a girl interrupt you while drinking apple juice.',
    ]
locations = [
    'Camp Cuddle',
    'Chonker’s Speedway',
    'Coney Crossroads',
    'Condo Canyon',
    'Command Cavern',
    'Greasy Grove',
    'Logjam Lumberyard',
    'Sleepy Sound',
    'Shifty Shafts',
    'Sanctuary',
    'Rockey Reels',
    'Tilted Towers',
    'The Daily Bugle',
    'The Joneses',
    'Synapse Station',
    'The Fortress'
]

@client.event                                                                                                       #Ready event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.command()                                                                                                   #Ready event
async def voice(ctx):
    for voice in voices:
    # to get the info. about various voices in our PC 
        print("Voice:")
        print("ID: %s" %voice.id)
        print("Name: %s" %voice.name)
        print("Age: %s" %voice.age)
        print("Gender: %s" %voice.gender)
        print("Languages Known: %s" %voice.languages)

'''@client.event                                                                                                       #Unknown command error
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound ):
        await ctx.message.channel.send('Dali ve')'''


# def recv_decoded_audio(self, data):
#     if data.ssrc not in self.user_timestamps:
#         self.user_timestamps.update({data.ssrc: data.timestamp})
#         # Add silence when they were not being recorded.
#         silence = 0
#     else:
#         silence = data.timestamp - self.user_timestamps[data.ssrc] - 960
#         self.user_timestamps[data.ssrc] = data.timestamp

#     data.decoded_data = struct.pack("<h", 0) * silence * opus._OpusStruct.CHANNELS + data.decoded_data
#     while data.ssrc not in self.ws.ssrc_map:
#         time.sleep(0.05)
#     self.sink.write(data.decoded_data, self.ws.ssrc_map[data.ssrc]["user_id"])






# //Connection _audioClient = await voiceChannel.ConnectAsync(); //Can get exception timeout here _audioClient.SpeakingUpdated += SpeakingUpdated; //called when someone starts to speak (probably only once) _audioClient.StreamCreated += StreamCreated; _audioClient.StreamDestroyed += StreamDestroyed; _audioClient.Disconnected += VoiceDisconnected;

# //Loop through the existing audio streams //You'll get an input stream PER PERSON CONNECTED // (new streams will by dynamically added or destroyed, callbacks as above) audioInStreams.Clear(); foreach (var kv in _audioClient.GetStreams()) { audioInStreams.Add_DupesIgnored(new Tuple<ulong, AudioInStream>(kv.Key, kv.Value)); }

# When first connected you need to make your bot make a noise or you'll never get incoming stream updates.

# //Speaking await connection.SetSpeakingAsync(true); // send a speaking indicator [basically doesn't work] var audioOutStream = connection.CreateDirectPCMStream(AudioApplication.Voice, bitrate: 48000);

# int discordSampling = 48000; //PCM S16LE = PCM signed 16-bit little-endian int blocksPerSecond = 50; //20ms chunks

# byte[] buffer = new byte[2 * discordSampling / blocksPerSecond]; //1/50 second of data per packet => 960 byte pairs //Fill the buffer in pairs, signed little endian for (int i = 0; i < 20;i++) await audioOutStream.WriteAsync(buffer, 0, buffer.Length);

# //Listening

# //AudioInStream stream = ... if (stream.AvailableFrames > 0) { //Soak up and ignore all frammes: RTPFrame frame; CancellationToken token = new(); while (true) if (!stream.TryReadFrame(token, out frame)) break;

# }
















@client.command(pass_context = True)                                                                                #Join
async def join(ctx):
    channel = ctx.message.author.voice.channel
    current_channel = await channel.connect()
    # print(current_channel.endpoint)
    print(ctx.voice_client.channel)

@client.command(pass_context = True)                                                                                #Join
async def read(ctx):
    # subprocess.call(['ffmpeg', '-i', 'quote.mp3', 'quote.wav'])
    quote = "quote.wav"
    with sr.AudioFile(quote) as source:
        # listen for the data (load audio to memory)
        audio_data = r.record(source)
        # print(type(audio_data))
        # recognize (convert from speech to text)
        text = r.recognize_google(audio_data, language = 'en-EN')
        print(text)

@client.command(pass_context = True)                                                                                #Leave
async def leave(ctx):
    await ctx.guild.voice_client.disconnect()

@client.command()                                                                                                   #Inspire
async def inspire(ctx):
    quote = random.choice(sigmaQuotes)
    output = gTTS(text = quote, lang = language, slow = False)
    #converter.say(quote)
    #converter.runAndWait()
    output.save("quote.wav")
    voice = await ctx.message.author.voice.channel.connect()
    voice.play(discord.FFmpegPCMAudio(executable="C:/ffmpeg/ffmpeg.exe", source="C:/Bernard/quote.wav"))

@client.command()                                                                                                   #Inspire
async def location(ctx):
    quote = random.choice(locations)
    output = gTTS(text = quote, lang = language, slow = False)
    #converter.say(quote)
    #converter.runAndWait()
    #output.save("location.mp3")
    voice = await ctx.message.author.voice.channel.connect()
    #voice.play(discord.FFmpegPCMAudio(executable="C:/ffmpeg/ffmpeg.exe", source="C:/Bernard/location.mp3"))
    voice.play(output)

@client.command(name="ping")
async def ping(ctx: commands.Context):
    await ctx.send(f"Pong! {round(client.latency * 1000)}ms")

@client.command()
async def record(ctx):
    ctx.voice_client.start_recording(discord.sinks.WaveSink(), finished_callback, ctx)

@client.command()
async def fipo(ctx):
    voice = await ctx.message.author.voice.channel.connect()
    voice.play(discord.FFmpegPCMAudio(executable="C:/ffmpeg/ffmpeg.exe", source="C:/Bernard/recordings/fipo/crazy.mp3"))

@client.command()
async def dada(ctx):
    voice = await ctx.message.author.voice.channel.connect()
    voice.play(discord.FFmpegPCMAudio(executable="C:/ffmpeg/ffmpeg.exe", source="C:/Bernard/dada.mp3"))

@client.command()
async def irissiri(ctx):
    voice = await ctx.message.author.voice.channel.connect()
    voice.play(discord.FFmpegPCMAudio(executable="C:/ffmpeg/ffmpeg.exe", source="C:/Bernard/irissiri.mp3"))

@client.command()
async def viki(ctx):
    voice = await ctx.message.author.voice.channel.connect()
    voice.play(discord.FFmpegPCMAudio(executable="C:/ffmpeg/ffmpeg.exe", source="C:/Bernard/viki.mp3"))

@client.command()
async def pog(ctx):
    voice = await ctx.message.author.voice.channel.connect()
    voice.play(discord.FFmpegPCMAudio(executable="C:/ffmpeg/ffmpeg.exe", source="C:/Bernard/pog.wav"))

@client.command()
async def ford(ctx):
    voice = await ctx.message.author.voice.channel.connect()
    voice.play(discord.FFmpegPCMAudio(executable="C:/ffmpeg/ffmpeg.exe", source="C:/Bernard/ford.mp3"))

@client.command()
async def heheheha(ctx):
    voice = await ctx.message.author.voice.channel.connect()
    voice.play(discord.FFmpegPCMAudio(executable="C:/ffmpeg/ffmpeg.exe", source="C:/Bernard/he-he-he-ha.mp4"))

@client.command()
async def socialCredit(ctx):
    voice = await ctx.message.author.voice.channel.connect()
    voice.play(discord.FFmpegPCMAudio(executable="C:/ffmpeg/ffmpeg.exe", source="C:/Bernard/socialCredit.mp3"))

@client.command()
async def hehe(ctx):
    voice = await ctx.message.author.voice.channel.connect()
    voice.play(discord.FFmpegPCMAudio(executable="C:/ffmpeg/ffmpeg.exe", source="C:/Bernard/Hehe.mp3"))

@client.command()
async def salatata(ctx):
    voice = await ctx.message.author.voice.channel.connect()
    voice.play(discord.FFmpegPCMAudio(executable="C:/ffmpeg/ffmpeg.exe", source="C:/Bernard/salatata.mov"))

@client.command()
async def ballsack(ctx):
    voice = await ctx.message.author.voice.channel.connect()
    voice.play(discord.FFmpegPCMAudio(executable="C:/ffmpeg/ffmpeg.exe", source="C:/Bernard/ballsack.mp3"))

@client.command()
async def drut(ctx):
    voice = await ctx.message.author.voice.channel.connect()
    voice.play(discord.FFmpegPCMAudio(executable="C:/ffmpeg/ffmpeg.exe", source="C:/Bernard/recordings/drut/drut.mp4"))

@client.command()
async def shoa(ctx):
    voice = await ctx.message.author.voice.channel.connect()
    voice.play(discord.FFmpegPCMAudio(executable="C:/ffmpeg/ffmpeg.exe", source="C:/Bernard/SHOA.mp3"))

@client.command()
async def dateebavgaza(ctx):
    voice = await ctx.message.author.voice.channel.connect()
    voice.play(discord.FFmpegPCMAudio(executable="C:/ffmpeg/ffmpeg.exe", source="C:/Bernard/microphone-results"))

@client.command()
async def mooo(ctx):
    voice = await ctx.message.author.voice.channel.connect()
    voice.play(discord.FFmpegPCMAudio(executable="C:/ffmpeg/ffmpeg.exe", source="C:/Bernard/moo.mp4"))

async def finished_callback(sink, ctx):

    recorded_users = {
        f"<@{user_id}>": audio
        for user_id, audio in recording_sink.audio_data.items()
    }

    files = [discord.File(audio.file, f"{user_id}.{sink.encoding}") for user_id, audio in sink.audio_data.items()]

    await ctx.channel.send(f"Finished! Recorded audio for {', '.join(recorded_users.keys())}.", files=files)

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
        with sr.AudioFile("C:/Bernard/recording0.wav") as source:
            audio_data = r.record(source)
            text = r.recognize_google(audio_data, language = 'bg-BG', show_all = True)
            print(text)
            current_command = text
            await ctx.channel.send(text)
    

@client.command()
async def stop_recording(ctx):
    ctx.voice_client.stop_recording()


@client.command()
async def play(ctx, url):
    server = ctx.message.guild
    voice_client = ctx.message.author.voice.channel
    player = await voice_client.create_ytdl_player(url)
    players[server.id] = player
    player.start()


@client.event
async def on_voice_state_update(member, before, after):
    user = member.id
    voice_client = discord.utils.get(client.voice_clients, guild = member.guild)

    '''
    try:
        if after.requested_to_speak_at() is not None:
            print("gospod bog")
    except:
        print("ne e gospod")
    #if before.requested_to_speak_at() is not after.requested_to_speak_at():
        #print("gospod bog")
    voice_manager = discord.GetVoiceManager()
    inputMode = voice_manager.GetInputMode()
    if inputMode.Type == 1:
        print("da, gospod e")
        '''

    if user == boss:
        if after.channel is not None:
            if before.channel is None:
                await after.channel.connect()
            elif before.channel is not after.channel and voice_client is not None:
                await member.guild.voice_client.move_to(after.channel)
            elif before.channel is not after.channel and voice_client is None:
                await after.channel.connect()

client.run(TOKEN)