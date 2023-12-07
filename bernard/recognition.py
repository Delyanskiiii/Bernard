import threading
import speech_recognition as sr
import json
import wave
import time
from pydub import AudioSegment
from pydub.playback import play
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
        # self.model = Model(r"../model_small")
        self.recognize = True
        self.t = threading.Thread(target=self.get_data, args=())
        self.t.start()

    def get_data(self):
        # with sr.Microphone() as source:
        #     try:
        #         while True:  # repeatedly listen for phrases and put the resulting audio on the audio processing job queue
        #             print(sr.Recognizer().listen(source))
        #     except KeyboardInterrupt:  # allow Ctrl + C to shut down the program
        #         pass
        while self.recognize:
            data = self.queue.get()
            if data:
                if data.ssrc not in self.users:
                    self.users[data.ssrc] = User(self.player, self.voice, data.ssrc, self.client)

                self.users[data.ssrc].start_of_speech()
                self.users[data.ssrc].recognize(data.decoded_data)
            else:
                for user in self.users.values():
                    if user.talking == True and time.time() - 0.1 >= user.last:
                        print('End of user talking: {}'.format(time.time()))
                        user.end_of_speech()
                        user.recognize(None)
                    else:
                        user.counter = user.counter + 1

    def stop(self):
        self.recognize = False

class User():

    def __init__(self, player, voice, ssrc, client) -> None:
        self.ssrc = ssrc
        self.player = player
        self.client = client
        self.voice = voice
        self.silence = 0
        self.counter = 0
        self.data = b''
        self.last = time.time()
        self.words = []
        self.r = sr.Recognizer()
        self.talking = False
        # self.recognizer = KaldiRecognizer(model, 96000)
        # self.recognizer.SetWords(False)

    def start_of_speech(self):
        if not self.talking:
            self.talking = True
            self.data = b''

    def end_of_speech(self):
        self.talking = False


    def recognize(self, data):
        if data is None:
            # print(self.data)
            audio_data = sr.AudioData(self.data, sample_rate=48000, sample_width=2)
            # Create a WAV file and write audio data to it
            with wave.open("output.wav", 'wb') as wf:
                wf.setnchannels(audio_data.sample_width)
                wf.setsampwidth(audio_data.sample_width)
                wf.setframerate(audio_data.sample_rate)
                wf.writeframes(audio_data.frame_data)

            target_sample_rate = 48000
            audio_segment = AudioSegment(
                audio_data.frame_data,
                sample_width=audio_data.sample_width,
                frame_rate=96000,
                channels=2
            ).set_frame_rate(target_sample_rate)

            # Convert the resampled audio back to an AudioData object
            resampled_audio_data = sr.AudioData(
                audio_segment.raw_data,
                sample_rate=target_sample_rate,
                sample_width=audio_data.sample_width
            )
            print('End of file manipulation: {}'.format(time.time()))
            # with wave.open("output.wav", "wb") as wav_file:
            #     # Set audio parameters
            #     wav_file.setnchannels(2)
            #     wav_file.setsampwidth(2)
            #     wav_file.setframerate(48000)

            #     # Write audio data to the WAV file
            #     wav_file.writeframes(self.data)
            # print(audio_data)
        # if data
        # received audio data, now we'll recognize it using Google Speech Recognition
            try:
                # for testing purposes, we're just using the default API key
                # to use another API key, use `r.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY")`
                # instead of `r.recognize_google(audio)`
                # text = self.r.recognize_google(audio_data, language = 'en-IN', show_all = True )
                # print(text)
                # print(self.r.recognize_whisper(audio_data, language="english"))
                print("I thinks you said '" + self.r.recognize_google(resampled_audio_data, language = 'bg-BG') + "'")
                print('End of recognition: {}'.format(time.time()))
                # print("Google Speech Recognition thinks you said " + self.r.recognize_google(audio_data, language = "en-US"))
            except sr.UnknownValueError as e:
                print("Google Speech Recognition could not understand audio {}".format(e))
            except sr.RequestError as e:
                print("Could not request results from Google Speech Recognition service; {0}".format(e))
        else:
            self.data = self.data + data
            # print(self.data)s

        self.last = time.time()
        # audio_queue.task_done()  # mark the audio processing job as completed in the queue
        # if self.recognizer.AcceptWaveform(data):
        #     pass
        # else:
        #     partial = self.recognizer.PartialResult()
        #     data = json.loads(partial)
        #     if data["partial"] != '':
        #         self.player.play(self.voice, data["partial"])
        #         print(data["partial"])
        #         # self.words.append(data["partial"])
        #         self.recognizer.Reset()