import sys, discord
sys.dont_write_bytecode = True

from discord.ext import commands
from tokens import YOUR_BOT_TOKEN
from bernard import Bernard

def main():
    bernard = Bernard()
    intents = discord.Intents.default()
    client = commands.Bot(intents = intents)

    @client.event
    async def on_ready():
        print('{0.user} is online.'.format(client))
        bernard.init(client)

    @client.event
    async def on_voice_state_update(member, before, after):
        await bernard.voice.handle_state_update(member, before, after)

    client.run(YOUR_BOT_TOKEN)

if __name__ == "__main__":
    main()
