import speech_recognition as sr
from os import path
import pyttsx3
from text import hello_logic, main_logic, hangup_logic, forward_logic, opts


'''Ответ бота'''
def speak(what):
    print(what)
    speak_engine.say(what)
    speak_engine.runAndWait()
    speak_engine.stop()


'''Функция принимает первое аудио ответа на приветствие'''
def callback(audio):
    try:
        voice = r.recognize_google(audio, language="ru-RU").lower()
        print("Распознано: " + voice)

        if voice in opts["alias"]:
            cmd = voice
            execute_cmd(cmd)

    except sr.UnknownValueError:
        speak(hello_logic['hello_null '])
    except sr.RequestError as e:
        speak(hangup_logic[' hangup_null'])


'''Функция принимает ответ'''
def execute_cmd(cmd):
    if cmd == 'да':
        speak(main_logic['recommend_main'])
        callback_nums()

    elif cmd == 'нет':
        speak(hangup_logic['hangup_wrong_time'])

    elif cmd == 'занят':
        speak(hangup_logic['hangup_wrong_time'])

    elif cmd == 'еще раз':
        speak(hello_logic['hello_repeat'])
    else:
        speak(main_logic['recommend_main'])


'''Функция распознавания ответа на вопрос об оценке'''
def callback_nums():
    AUDIO_FILE = path.join(path.dirname(path.realpath(__file__)), "5.wav")
    with sr.AudioFile(AUDIO_FILE) as source:
        audio = r.record(source)
    voice = r.recognize_google(audio, language="ru-RU").lower()
    print("Распознано: " + voice)
    try:

        otvet_recommend(voice)

    except sr.UnknownValueError:
        speak(main_logic['recommend_default'])
    except sr.RequestError as e:
        print(hangup_logic['hangup_null'])

'''Принимает ответ на вопрос'''
def otvet_recommend(voice):
    if voice == 'нет':
        speak(main_logic['recommend_score_negative'])
    elif voice == 'да':
        speak(main_logic['recommend_score_positive'])
    elif voice == 'возможно':
        speak(main_logic['recommend_score_neutral'])
    elif voice == 'еще раз':
        speak(main_logic['recommend_repeat'])
    elif voice == 'не знаю':
        speak(main_logic['recommend_repeat_2'])
    elif voice == 'занят':
        speak(hangup_logic['hangup_wrong_time'])
    elif voice == 'вопрос':
        speak(forward_logic['forward'])
    else:
        i = 0
        for k in opts['nums']:
            if voice == str(k):
                i = k
        if voice == str(i):
            if i >= 0 and i <= 8:
                speak(hangup_logic['hangup_negative'])
            else:
                speak(hangup_logic['hangup_positive'])
        else:
            speak(main_logic['recommend_default'])


AUDIO_FILE = path.join(path.dirname(path.realpath(__file__)), "da.wav")
r = sr.Recognizer()

with sr.AudioFile(AUDIO_FILE) as source:
    audio = r.record(source)

speak_engine = pyttsx3.init()
speak(hello_logic['hello'])
callback(audio)
