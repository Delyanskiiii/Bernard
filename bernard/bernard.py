import time, queue
import threading
from player import Player
from user import User
import discord
import re
import asyncio

class Bernard():

    def __init__(self):
        self.ssrc_map = {}
        self.mute_timer = 0
        self.q = None
        self.voice = None
        self.client = None
        self.users = {}
        self.command_queue = queue.Queue()
        self.player = None
        self.recognize = False
        self.commands = {
            ['play', 'пусни']: self.player.play(),
            ['pause', 'пауза']: self.player.pause(),
            ['resume', 'продължи']: self.player.resume(),
            ['stop', 'спри']: self.player.stop(),
            ['skip', 'следваща']: self.player.skip(),
        }

    def set_client(self, client):
        self.client = client

    async def setup(self):
        if not self.recognize:
            self.recognize = True
            self.t = threading.Thread(target=self.get_data, args=())
            self.t.start()

    def get_data(self):
        while self.recognize:
            data = self.q.get()
            if data:
                if data.ssrc not in self.users:
                    self.users[data.ssrc] = User(self.command_queue)

                self.users[data.ssrc].feed_data(data)
            else:
                for user in self.users.values():
                    if user.talking == True and user.transcribing == False and time.time() - 0.1 >= user.last_fed:
                        user.thread()

            if not self.command_queue.empty():
                self.command(self.command_queue.get_nowait())
        # await self.leave_voice()

    def command(self, commands):
        print(commands)
        for command in commands:
            words = command.split()
        if command[0]:
            pattern = r'(\d+)%'
            match = re.search(pattern, command[0])

            if match:
                self.player.set_volume(float(match.group(1)) / 100)

            if 'майка' in command[0]:
                self.player.play(discord.FFmpegPCMAudio(executable="C:/ffmpeg/ffmpeg.exe", source="../voice/system/steel.mp3"))
            if 'чакай' in command[0]:
                self.player.pause()
            if 'давай' in command[0]:
                self.player.resume()
            if 'стига' in command[0]:
                self.player.stop()

        if command[1]:
            self.player.play(command[1])
            # if 'octane' in command[1] or 'murder in my' in command[1]:
            #     self.player.play(discord.FFmpegPCMAudio(executable="C:/ffmpeg/ffmpeg.exe", source="../voice/system/murder.mp3"))
            # if "that's enough" in command[1]:
            #     self.recognize = False

    async def join_voice(self, channel):
        self.voice = await channel.connect()
        self.q = queue.Queue()
        self.voice.start_listening(self.q)
        self.player = Player(self.voice)
        await self.setup()

    async def leave_voice(self):
        self.player.stop()
        self.voice.stop_listening()
        self.recognize = False
        await self.voice.disconnect()
        self.q = None
        self.voice = None
        self.player = None

    async def handle_state_update(self, member, before, after):
        print(self.ssrc_map)

        if self.voice and self.voice.ws:
            self.ssrc_map = self.voice.ws.ssrc_map

        if before.self_mute != after.self_mute and after.channel and self.voice is None:
            now = time.time()

            if now - 1 <= self.mute_timer:
                await self.join_voice(after.channel)

            self.mute_timer = now

        if self.voice and len(self.voice.channel.members) == 1:
            await self.leave_voice()
