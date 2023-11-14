import threading
import speech_recognition as sr
from vosk import Model, KaldiRecognizer
from tokens import silence

class Recoginition_Manager():

    def __init__(self, queue) -> None:
        self.users = {}
        self.queue = queue
        self.recognize = True
        self.t = threading.Thread(target=self.get_data, args=())
        self.t.start()

    def get_data(self):
        while self.recognize:
            data = self.queue.get()
            if data:
                if data.ssrc not in self.users:
                    self.users[data.ssrc] = User(data.ssrc)

                self.users[data.ssrc].recognize(data.decoded_data)
            
            else:
                for user in self.users.values():
                    user.recognize(silence)

    def stop(self):
        self.recognize = False

class User():

    def __init__(self, ssrc) -> None:
        print('init')
        self.ssrc = ssrc
        # self.recognizer = sr.Recognizer()
        model = Model(r"../model_small")
        self.recognizer = KaldiRecognizer(model, 96000)
        self.recognizer.SetWords(False)

    def recognize(self, data):
        if self.recognizer.AcceptWaveform(data):
            result = self.recognizer.Result()
            print(result)
        # audio_data = sr.AudioData(data, frame_rate=90000, sample_width=2)
        # try:
        #     # Recognize speech using Google Web Speech API
        #     text = self.recognizer.recognize_google(audio_data)
        #     print(text)
        # except sr.UnknownValueError:
        #     print("Google Web Speech API could not understand audio")
        # except sr.RequestError as e:
        #     print(f"Could not request results from Google Web Speech API; {e}")