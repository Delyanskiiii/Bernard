import time, queue
import threading
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
        self.advanced_commands = None

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
                        user.transcribe_data()

            if not self.command_queue.empty():
                self.command(self.command_queue.get_nowait())

    def command(self, commands):
        for command in commands:
            if command:
                for word in self.advanced_commands:
                    start_index = command.find(word)

                    if start_index != -1:
                        print(command[start_index + len(word):])
                        self.player.play(command[start_index + len(word):])
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
            'pause пауза': self.player.pause,
            'resume продължи': self.player.resume,
            'stop спри': self.player.stop,
            'skip следваща': self.player.skip,
        }
        self.advanced_commands = ['play', 'пусни']
        await self.setup()

    async def leave_voice(self):
        self.player.stop()
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
