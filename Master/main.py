import time
import serial
import threading
from vosk import Model, KaldiRecognizer
import pyaudio

from tts import say
from decode import decrypt
from encode import encrypt
import bluetooth_handler

recvd_morse_code = ''
recv = ''
capture_audio = True

RED_COLOR   = "\033[91m"
GREEN_COLOR = "\033[92m"
RESET_COLOR = "\033[0m"

try:
    ser = serial.Serial(port='/dev/rfcomm0', baudrate=9600)
    
except Exception:
    
    while 1:
        print("Connection is not established!")
        time.sleep(1)
        
ser.isOpen()

settings = "r" #ping the slave unit
settings = settings + '\n'
ser.write(settings.encode())

print("In Main Thread")


def speech_recognition():
    model = Model(r"/home/pi/Master/vosk-model-small-en-in-0.4")
    recognizer = KaldiRecognizer(model, 16000)
    mic = pyaudio.PyAudio()

    stream = mic.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=8192)
    stream.start_stream()
    print("\nSpeech recognition module is running...")
    
    print(RED_COLOR + "DASH to disable Speech recognition" + RESET_COLOR)
    print(GREEN_COLOR + "DOT to enable Speech recognition" + RESET_COLOR)
    
    while True:
        try:

            data = stream.read(4096)
            #print("Capture audio: ", capture_audio)
            
            if capture_audio:
                if recognizer.AcceptWaveform(data):
                    text = recognizer.Result()
                    response = text[14:-3]
                    
                    if len(response) > 0:
                        print(response)
                        
                        if(response.upper() == "SILENT"):
                            print(RED_COLOR + "Slave device set to silent mode" + RESET_COLOR)
                            settings = "s"
                            settings = settings + '\n'
                            ser.write(settings.encode())
                        else:
                            morse_to_avr = encrypt(response)
                            print(morse_to_avr) #TEXT to MORSE
                            
                            morse_to_avr = morse_to_avr + '\n'
                            ser.write(morse_to_avr.encode())
                            
                    else:
                        print(RED_COLOR + "." + RESET_COLOR)
        except OSError:
            pass
    


speech_thread = threading.Thread(target=speech_recognition)
speech_thread.start()


while 1 :

    if ser.inWaiting() > 0:
        recv = ser.readline()

    if recv != '':
        
        recvd_morse_code = str(recv, 'utf-8').strip()
        print("Received morse code: ",recvd_morse_code)
        
        translated_content = decrypt(recvd_morse_code)
        print("Translated content: ",translated_content)
        
        
        if(translated_content == "E"): #DOT
            print("Voice recognition Activated")
            say("Voice recognition Activated", language='en-US')
            capture_audio = True
            
        elif(translated_content == "T"): #DASH
            print("Voice recognition deactivated")
            say("Voice recognition deactivated", language='en-US')
            capture_audio = False
        else:
            say(translated_content, language='en-US')
            
            
        
       # print(decrypt(".... . .-.. .-.. ---"))
        recv = ''
        
        
speech_thread.join()
if bluetooth_auto_reconnect.threadStatus:
    print("Bluetooth Thread joined")
    thread.join()