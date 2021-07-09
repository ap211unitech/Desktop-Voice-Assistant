import pyttsx3
import datetime
import speech_recognition as sr
import wikipedia
import webbrowser
import os
import smtplib
import pyjokes
import time

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
        r.pause_threshold = 1
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
        if 'greet me' in query:
            wiseMe()

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

        elif 'open interviewbit' in query:
            openWebBrowser('interviewbit.com')

        elif 'open vscode' in query:
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
            openWebBrowser('https://www.google.com/search?q='+query)

        elif 'play' in query:
            query = query.replace("play", "")
            openWebBrowser('https://www.youtube.com/search?q='+query)

        elif "don't listen" in query or "stop listening" in query:
            speak("for how much time you want to stop jarvis from listening commands")
            a = int(input())
            time.sleep(a)
            print(a)

        elif 'shutdown jarvis' in query or 'shutdown' in query:
            speak("Thanks for giving me your time sir")
            exit()

        else:
            if query != 'none':
                openWebBrowser('https://www.google.com/search?q='+query)
