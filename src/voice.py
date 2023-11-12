import time, queue

class Voice():

    def __init__(self, client):
        self.ssrc_map = {}
        self.mute_timer = 0
        self.q = None
        self.voice = None
        self.client = client
        self.busy = False
        self.follow = None

    async def join_voice(self, channel):
        self.voice = await channel.connect()
        self.q = queue.Queue()
        self.voice.start_listening(self.q)
        print('start listening')

    async def leave_voice(self):
        self.voice.stop_listening()
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