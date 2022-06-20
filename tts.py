import tika
from tika import parser
from random import randint
# import pyttsx3
from gtts import gTTS
import os

def convert(file_path):
    tika.initVM()
    parsed_pdf = parser.from_file(file_path)
    content = parsed_pdf['content'].strip()
    content = content.replace('\n', ' ')
    # print(content)
    
    audio_name = 'audio.mp3'
    # engine = pyttsx3.init()
    # engine.setProperty('rate', 150)
    # engine.say(content)

    # engine.save_to_file(content, audio_name)
    # engine.runAndWait()
    # os.system(f'start {audio_name}')

    audio = gTTS(content)
    audio.save(audio_name)

if __name__ == "__main__":
    convert('file.pdf')