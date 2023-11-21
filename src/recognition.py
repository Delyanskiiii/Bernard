import threading
import speech_recognition as sr
import json
from player import Player
from vosk import Model, KaldiRecognizer, SetLogLevel
SetLogLevel(-1)
from tokens import silence

class Recoginition_Manager():

    def __init__(self, queue, voice, client) -> None:
        self.users = {}
        self.voice = voice
        self.player = Player()
        self.client = client
        self.queue = queue
        self.model = Model(r"../model_small")
        self.recognize = True
        self.t = threading.Thread(target=self.get_data, args=())
        self.t.start()

    def get_data(self):
        while self.recognize:
            data = self.queue.get()
            if data:
                if data.ssrc not in self.users:
                    self.users[data.ssrc] = User(self.player, self.voice, data.ssrc, self.client, self.model)

                self.users[data.ssrc].recognize(data.decoded_data)

    def stop(self):
        self.recognize = False

class User():

    def __init__(self, player, voice, ssrc, client, model) -> None:
        self.ssrc = ssrc
        self.player = player
        self.client = client
        self.voice = voice
        self.silence = 0
        self.words = []
        self.recognizer = KaldiRecognizer(model, 96000)
        # self.recognizer.SetWords(False)

    def recognize(self, data):
        if self.recognizer.AcceptWaveform(data):
            pass
        else:
            partial = self.recognizer.PartialResult()
            data = json.loads(partial)
            if data["partial"] != '':
                self.player.play(self.voice, data["partial"])
                print(data["partial"])
                # self.words.append(data["partial"])
                self.recognizer.Reset()