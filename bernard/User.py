import time
import threading
import speech_recognition as sr

from pydub import AudioSegment
from queue import Queue

class User():
    '''Represents user in voice channel.
    Handles all the data for it's user and transcribes it.
    Returns the bulgarian transcription.
    '''
    def __init__(self) -> None:
        self.data = b''
        self.transcribing = False
        self.talking = False
        self.last_fed = time.time()
        self.r = sr.Recognizer()

    def feed_data(self, data):
        if not self.talking:
            self.data = b''
            self.talking = True
        self.data = self.data + data.decoded_data
        self.last_fed = time.time()

    def thread(self):
        self.talking = False
        self.transcribing = True

        queue = Queue()
        thread = threading.Thread(target=self.transcribe, args=(queue,),)
        thread.start()

        thread.join()
        self.transcribing = False

        return queue.get()

    def transcribe(self, queue):
        audio_segment = AudioSegment(
            self.data,
            sample_width=2,
            frame_rate=96000,
            channels=2
        ).set_frame_rate(48000)

        audio_data = sr.AudioData(
            audio_segment.raw_data,
            sample_rate=48000,
            sample_width=2
        )

        commands = []
        try:
            commands.append(self.r.recognize_google(audio_data, language = 'bg-BG'))
        except:
            commands.append(None)
        try:
            commands.append(self.r.recognize_google(audio_data, language = 'en-EN'))
        except:
            commands.append(None)

        queue.put(commands)