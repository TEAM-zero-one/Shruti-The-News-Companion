from gtts import gTTS
import os

def generate_audio(text, filename="summary_audio.mp3"):
    tts = gTTS(text, lang='en-uk')
    tts.save(filename)
    return filename