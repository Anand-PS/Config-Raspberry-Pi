import subprocess

def say(text, language='en-US'):
    wav_file = "/tmp/tts.wav"

    # Run the pico2wave command to synthesize speech with the specified language code
    subprocess.run(['pico2wave', '-l', language, '-w', wav_file, text])

    # Play the audio using aplay command
    subprocess.run(['aplay', wav_file])

    # Remove the temporary WAV file
    subprocess.run(['rm', wav_file])
