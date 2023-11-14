import time, queue
from voice import Voice
from recognition import Recoginition_Manager

class Bernard():

    def __init__(self):
        self.ssrc_map = {}
        self.mute_timer = 0
        self.q = None
        self.voice = None
        self.client = None
        self.busy = False
        self.follow = None
        self.recognition = None

    def set_client(self, client):
        self.client = client

    async def join_voice(self, channel):
        self.voice = await channel.connect()
        self.q = queue.Queue()
        self.voice.start_listening(self.q)
        self.recognition = Recoginition_Manager(self.q)
        print('start listening')

    async def leave_voice(self):
        self.voice.stop_listening()
        self.recognition.stop()
        self.recognition = None
        print('stop listening')
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