import time, queue
import threading
import asyncio
from player import Player
from user import User

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
        self.simple_commands = None
        self.play_commands = None
        self.leave_commands = None

    def set_client(self, client):
        self.client = client

    def between_callback(self):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

        loop.run_until_complete(self.get_data())
        loop.close()

    async def setup(self):
        if not self.recognize:
            self.recognize = True
            # future = asyncio.Future()
            # asyncio.create_task(self.get_data())
            self.t = threading.Thread(target=self.between_callback, args=())
            self.t.start()

            # result = await future
            # if result:
            #     await self.leave_voice()

    async def get_data(self):
        while self.recognize:
            data = self.q.get()
            if data:
                if data.ssrc not in self.users:
                    self.users[data.ssrc] = User(self.command_queue)

                self.users[data.ssrc].feed_data(data)
            else:
                for user in self.users.values():
                    if user.talking == True and user.transcribing == False and time.time() - 0.1 >= user.last_fed:
                        user.transcribe_data()

            if not self.command_queue.empty():
                await self.command(self.command_queue.get_nowait())
        
        # future.set_result(True)

    async def command(self, commands):
        for command in commands:
            if command:
                for word in self.play_commands:
                    start_index = command.find(word)

                    if start_index != -1:
                        print(command[start_index + len(word) + 1:])
                        loop = asyncio.get_event_loop()
                        await self.player.play(command[start_index + len(word):], loop)
                        return
                    
                for word in self.leave_commands:
                    start_index = command.find(word)

                    if start_index != -1:
                        print(word)
                        self.recognize = False
                        return

                words = command.split()
                for word in words:
                    for key, value in self.simple_commands.items():
                        list = key.split()
                        if word in list:
                            print(word)
                            value()
                            return

    async def join_voice(self, channel):
        self.voice = await channel.connect()
        self.q = queue.Queue()
        self.voice.start_listening(self.q)
        self.player = Player(self.voice)
        self.simple_commands = {
            'pause пауза паузирай': self.player.pause,
            'resume продълж': self.player.resume,
            'skip следваща stop спри': self.player.skip,
        }
        self.play_commands = ['play', 'пусни']
        self.leave_commands = ["that's enough", 'leave']
        await self.setup()

    async def leave_voice(self):
        self.voice.stop_listening()
        self.recognize = False
        await self.voice.disconnect()
        self.q = None
        self.voice = None
        self.commands = None
        self.player = None

    async def handle_state_update(self, member, before, after):
        if self.voice and self.voice.ws:
            self.ssrc_map = self.voice.ws.ssrc_map

        if before.self_mute != after.self_mute and after.channel and self.voice is None:
            now = time.time()

            if now - 1 <= self.mute_timer:
                await self.join_voice(after.channel)

            self.mute_timer = now

        if self.voice and len(self.voice.channel.members) == 1:
            await self.leave_voice()
