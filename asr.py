import speech_recognition as sr


def Recognize(audio_file):
    r = sr.Recognizer()

    audioFile = sr.AudioFile(audio_file)

    with audioFile as source:
        audio = r.record(source)
            
    text = r.recognize_google(audio)

    return(text)