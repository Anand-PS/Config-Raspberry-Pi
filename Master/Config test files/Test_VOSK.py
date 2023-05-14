from vosk import Model, KaldiRecognizer
import pyaudio
import threading
import time



def speech_recognition():
    model = Model(r"/home/pi/Master/vosk-model-small-en-in-0.4")
    recognizer = KaldiRecognizer(model, 16000)
    mic = pyaudio.PyAudio()

    stream = mic.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=8192)
    stream.start_stream()
    print("\nSpeech recognition module is running...")

    while True:
        try:
                          
                data = stream.read(4096)
                    
                if recognizer.AcceptWaveform(data):
                    text = recognizer.Result()
                    response = text[14:-3]
                    if len(response) > 0:
                        print(response)
                    else:
                        print(".")
        except OSError:
            pass

speech_thread = threading.Thread(target=speech_recognition)
speech_thread.start()