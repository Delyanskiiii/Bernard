import sys, os, discord
sys.dont_write_bytecode = True

from discord.ext import commands
from bernard import Bernard

def main():
    token = os.getenv('BOT_TOKEN')
    if token is None:
        print("Can't find bot token")
        return

    bernard = Bernard()
    intents = discord.Intents.default()
    client = commands.Bot(intents = intents)

    @client.event
    async def on_ready():
        print('{0.user} is online.'.format(client))
        bernard.set_client(client)

    @client.event
    async def on_voice_state_update(member, before, after):
        await bernard.handle_state_update(member, before, after)

    client.run(token)

if __name__ == "__main__":
    main()
