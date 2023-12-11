import time, queue
import threading
from player import Player
from User import User

class Bernard():

    def __init__(self):
        self.ssrc_map = {}
        self.mute_timer = 0
        self.q = None
        self.voice = None
        self.client = None
        self.users = {}
        self.player = None
        self.recognize = False

    def set_client(self, client):
        self.client = client

    def setup(self):
        if not self.recognize:
            self.recognize = True
            self.t = threading.Thread(target=self.get_data, args=())
            self.t.start()

    def get_data(self):
        while self.recognize:
            data = self.q.get()
            if data:
                if data.ssrc not in self.users:
                    self.users[data.ssrc] = User()

                self.users[data.ssrc].feed_data(data)
            else:
                for user in self.users.values():
                    if user.talking == True and user.transcribing == False and time.time() - 0.1 >= user.last_fed:
                        print(user.thread())

    async def join_voice(self, channel):
        self.voice = await channel.connect()
        self.q = queue.Queue()
        self.voice.start_listening(self.q)
        self.player = Player(self.voice)
        self.setup()

    async def leave_voice(self):
        self.voice.stop_listening()
        self.recognize = False
        await self.voice.disconnect()
        self.q = None
        self.voice = None

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
