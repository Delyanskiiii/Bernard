from voice import Voice

class Bernard():

    def __init__(self):
        self.client = None
        self.voice = None

    def init(self, client):
        self.client = client
        self.voice = Voice(client)
