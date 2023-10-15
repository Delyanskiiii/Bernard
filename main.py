import sys
sys.dont_write_bytecode = True
import discord
import asyncio
from discord.ext import commands
from tokens import YOUR_BOT_TOKEN, BOSS_ID

intents = discord.Intents.default()
intents.message_content = True
client = commands.Bot(intents = intents, command_prefix = '.')

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.command(pass_context = True)
async def join(ctx):
    voice = await ctx.message.author.voice.channel.connect()
    while voice.is_connected():
        try:
            voice_packet = voice.socket.recv(4096)  # Receive audio data (adjust buffer size as needed)
            ctx.voice_client.play(discord.FFmpegPCMAudio(executable="C:/ffmpeg/ffmpeg.exe", source="./voice/fipo/crazy.mp3"))

        except BlockingIOError as e:
            print('shoa')
            print('_')
            await asyncio.sleep(0.1)

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