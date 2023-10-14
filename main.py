import sys
sys.dont_write_bytecode = True
import discord
from discord.ext import commands
from bot_token import YOUR_BOT_TOKEN

intents = discord.Intents.default()
intents.message_content = True
client = commands.Bot(intents = intents, command_prefix = '.')

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.command(pass_context = True)
async def join(ctx):
    await ctx.message.author.voice.channel.connect()

@client.command(pass_context = True)
async def leave(ctx):
    await ctx.guild.voice_client.disconnect()

@client.command()
async def fipo(ctx):
    ctx.voice_client.play(discord.FFmpegPCMAudio(executable="C:/ffmpeg/ffmpeg.exe", source="./voice/fipo/crazy.mp3"))

client.run(YOUR_BOT_TOKEN)