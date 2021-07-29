import pyttsx3
import datetime
import speech_recognition as sr
import wikipedia
import webbrowser
import os
import json
import smtplib
import pyjokes
import time
import winshell
import subprocess
from ecapture import ecapture as ec
from urllib.request import urlopen


engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)


def speak(audio):
    engine.say(audio)
    engine.runAndWait()


def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 0.4
        r.non_speaking_duration = 0.4
        # r.energy_threshold = 100
        audio = r.listen(source)
    try:
        print('Recognizing...')
        query = r.recognize_google(audio, language='en-in')
        print(f"User said: {query}\n")
    except Exception as e:
        print(e)
        print('Say that again please...')
        return "None"
    return query


def openWebBrowser(query):
    webbrowser.register('chrome',
                        None,
                        webbrowser.BackgroundBrowser("C://Program Files (x86)//Google//Chrome//Application//chrome.exe"))
    webbrowser.get('chrome').open(query)


def sendEmail(to, content):
    f = open("password.txt", "r")
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.login('porwal.1@iitj.ac.in', str(f.read()))
    server.sendmail('porwal.1@iitj.ac.in', to, content)
    server.close()


def wiseMe():
    hour = int(datetime.datetime.now().hour)
    if hour >= 0 and hour < 12:
        speak('Good Morning sir')
    elif hour >= 12 and hour <= 18:
        speak('Good after noon sir')
    else:
        speak('Good evening sir')

    speak('I am Jarvis, how may i help you')


if __name__ == '__main__':
    wiseMe()
    while True:
        # query = input()
        query = takeCommand().lower()
        if 'greet me' in query or 'wish me' in query:
            wiseMe()

        elif 'who are you' in query or 'what can you do' in query:
            speak('''I am Jarvis, version 1 point O, your personal assistant. I am programmed to do some daily tasks like
                  opening youtube, google chrome, gmail and stackoverflow, take a photo, search wikipedia, predict weather in different cities, get top headline news etc. but I can do further more tasks,
                  I am under progress till now''')

        elif "who made you" in query or "who created you" in query or "who discovered you" in query:
            speak("I was built by Arjun")

        elif "wikipedia" in query:
            speak('Searching Wikipedia...')
            query = query.replace("wikipedia", "")
            results = wikipedia.summary(query, sentences=2)
            speak("According to Wikipedia: ")
            print(results)
            speak(results)

        elif 'open youtube' in query:
            openWebBrowser('youtube.com')

        elif 'open google' in query:
            openWebBrowser('google.com')

        elif 'open gmail' in query:
            openWebBrowser("gmail.com")

        elif 'open interviewbit' in query:
            openWebBrowser('interviewbit.com')

        elif 'open vscode' in query or 'open vs code' in query:
            codePath = "C:\\Users\\AP\\AppData\\Local\\Programs\\Microsoft VS Code\\Code.exe"
            os.startfile(codePath)

        elif 'send email' in query:
            try:
                speak("Please tell recipient email.")
                to = input()
                speak("Please tell subject of email.")
                subject = takeCommand()
                speak("What should i say to him?")
                content = takeCommand()
                message = 'Subject: {}\n\n{}'.format(subject, content)
                sendEmail(to, message)
                speak("Email has been sent!")
            except Exception as e:
                print(e)
                speak("Sorry sir, I am not able to send this email")

        elif 'joke' in query:
            joke = pyjokes.get_joke()
            print(joke)
            speak(joke)

        elif 'search' in query:
            query = query.replace("search", "")
            query = query.replace("for", "")
            openWebBrowser('https://www.google.com/search?q='+query)

        elif 'play' in query or 'music' in query:
            query = query.replace("play", "")
            query = query.replace("music", "")
            query = query.replace("of", "")
            openWebBrowser('https://www.youtube.com/search?q='+query)

        elif 'news' in query:
            try:
                jsonObj = urlopen(
                    '''https://newsapi.org/v1/articles?source=the-times-of-india&sortBy=top
                    &apiKey=f599182c822d4b7dbad3e2d30d608385''')
                data = json.load(jsonObj)
                i = 1

                speak('here are some top news from the times of india')
                print('''=============== TIMES OF INDIA ============''' + '\n')

                for item in data['articles']:
                    print(str(i) + '. ' + item['title'] + '\n')
                    print(item['description'] + '\n')
                    speak(str(i) + '. ' + item['title'] + '\n')
                    i += 1
            except Exception as e:
                print(str(e))

        elif "write a note" in query or "take a note" in query:
            speak("What should i write, sir")
            note = takeCommand()
            file = open('jarvis.txt', 'w')
            speak("Sir, Should i include date and time")
            snfm = takeCommand()
            if 'yes' in snfm or 'sure' in snfm:
                strDateTime = datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
                file.write(strDateTime)
                file.write(" :- ")
                file.write(note)
            else:
                file.write(note)
            speak('Note Taken')

        elif "show note" in query or "show my previous note" in query:
            speak("Showing Notes")
            file = open("jarvis.txt", "r")

            note = file.read()
            print(note)
            try:
                k = int(note[0])
                speak('You have written, '+note[24:])
            except:
                speak('You have written, '+note)

        elif "camera" in query or "take a photo" in query:
            ec.capture(0, "Jarvis Camera ", "img.jpg")

        elif "don't listen" in query or "stop listening" in query:
            speak("for how much time you want to stop jarvis from listening commands")
            a = int(input())
            time.sleep(a)
            print(a)

        elif 'empty recycle bin' in query:
            winshell.recycle_bin().empty(confirm=False, show_progress=False, sound=True)
            speak("Recycle Bin Recycled")

        elif 'shutdown system' in query:
            speak("Hold On a Sec ! Your system is on its way to shut down")
            subprocess.call('shutdown /p /f')
            exit()

        elif "hibernate" in query or "sleep" in query:
            speak("Hibernating")
            subprocess.call("shutdown /h")
            exit()

        elif 'shutdown jarvis' in query or 'shutdown' in query:
            speak("Thanks for giving me your time sir")
            exit()

        else:
            print('Sorry sir, I am unable to find this')
