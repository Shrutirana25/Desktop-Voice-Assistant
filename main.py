import pyttsx3
import speech_recognition as sr
import datetime
import appControl
import wikipedia
import normalChat 
import webbrowser
import webScrapping
from threading import Thread
import requests
from deep_translator import GoogleTranslator
from googletrans import LANGUAGES
import ToDo

engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)
voice_id = 0  # 0 for female, 1 for male
ass_volume = 1  # max volume
ass_voiceRate = 200
ownerDesignation = "sir"
Name="kashish"

def isContain(txt, lst):
    for word in lst:
        if word in txt:
            return True
    return False

def speak(audio) -> object:
    engine.say(audio)
    engine.runAndWait()

def takecommand():
    r = sr.Recognizer()
    r.dynamic_energy_threshold = False
    r.energy_threshold = 300
    r.pause_threshold = 0.6
    r.non_speaking_duration = 0.5
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source)
        print("Listening...")
        audio = r.listen(source)

    try:
        print("recognizing.....")
        query = r.recognize_google(audio, language='en-in')
        print(f"user said: {query}\n")
    except Exception as e:
        print(e)
        print("say that again please.....")
        return "None"
    return query

def wishme():
    hour = int(datetime.datetime.now().hour)
    if hour > 0 and hour < 12:
        speak("Good morning")
    elif hour >= 12 and hour < 18:
        speak("Good afternoon")
    else:
        speak("Good evening")
    print("Hi, my name is Taara, and how may I help you?")
    speak("Hi, my name is Taara, and how may I help you?")
    global Name
    print("Enter your Name to start")
    speak("Enter your Name to start")
    Name = input()
    speak("Enter your Gender")
    print("Enter your Gender (F,f=FEMALE , M,m=MALE)")
    Gender = input().lower()
    print("Name = " + Name)
    print("Gender = " + Gender)
    global ownerDesignation
    if Gender == "m":
        ownerDesignation = "Sir"
    else:
        ownerDesignation = "Ma'am"

def translate_text(sentence, dest_language_code):
    try:
        translated = GoogleTranslator(source='auto', target=dest_language_code).translate(sentence)
        return translated
    except Exception as e:
        print(f"Translation failed: {e}")
        return None


if __name__ == '__main__':
    wishme()
    while True:
        query = takecommand().lower()

        ############# Normal Things 

        if "hello" in query:
            print("Hello, how are you?")
            speak("Hello, how are you?")

        elif "time" in query or "date" in query:
            response = normalChat.chat(query)
            print(response)
            speak(response)

        elif 'morning' in query or 'evening' in query or ('noon' in query and 'good' in query):
            response = normalChat.chat("good")
            print(response)
            speak(response)

        elif "fine" in query or "very nice" in query:
            print("Great, so how can I help you?")
            speak("Great, so how can I help you?")

        elif 'the time' in query or "time" in query:
            strtime = datetime.datetime.now().strftime("%H:%M:%S")
            print(strtime)
            speak(f"The time is {strtime}")

        elif 'battery' in query or 'system info' in query:
            result = appControl.OSHandler(query)
            if len(result) == 2:
                print(result[0])
                speak(result[0])
                print(result[1])
                print(result)
            else:
                speak(result)    
        # IP ADDRESS
        elif "ip address" in query:
            ip = requests.get('https://api.ipify.org').text
            print(ip)
            speak(f"Your ip address is {ip}")    

        ################  WIKIPEDIA
        elif 'wikipedia' in query:
            speak("Searching Wikipedia...")
            query = query.replace("wikipedia", "")
            results = wikipedia.summary(query, sentences=1)
            print(results)
            speak("According to Wikipedia")
            speak(results)

        ############## Open APPS close type things
        elif isContain(query, ['open', 'type', 'save', 'delete', 'select', 'press enter']):
            appControl.System_Opt(query)

        elif isContain(query, ['window', 'close that', 'close window', 'close']):
            appControl.Win_Opt(query)

        ############### CHANGE VOICE         
        elif "voice" in query:
            try:
                if 'female' in query:
                    voice_id = 1
                elif 'male' in query:
                    voice_id = 0
                else:
                    voice_id = 1 if voice_id == 0 else 0
                engine.setProperty('voice', voices[voice_id].id)
                speak(f"Hello {ownerDesignation}, I have changed my voice. How may I help you?")
            except Exception as e:
                print(e)

        ############### Send Email               
        elif 'email' in query:
            print("Enter the Receiver's Email ID")
            speak('Whom do you want to send the email to?')
            rec_email = input()
            speak('What is the subject?')
            subject = takecommand()
            speak('What message do you want to send?')
            message = takecommand()
            Thread(target=webScrapping.email, args=(rec_email, message, subject)).start()
            speak('Email has been sent successfully')

        ############ Specfic Youtube Video            
        elif isContain(query, ['youtube', 'video']):
            speak("Okay, here is a video kfor you...")
            try:
                speak(webScrapping.youtube(query))
            except Exception as e:
                print(e)
                speak("Desired result not found")
                    
        ############# Open Website       
        elif 'open youtube' in query:
            try:
                webbrowser.open("youtube.com")
            except:
                speak("Please try that again")

        elif 'open chrome' in query:
            webbrowser.open("google.com")

        elif 'open stack overflow' in query:
            webbrowser.open_new_tab("https://stackoverflow.com/")
            speak("Here is StackOverflow")
        ########## Weather and Temprature
        elif "temperature" in query:
            speak("whats the city name")
            location = takecommand()
            if location != "None":
                try:
                    complete_api_link = "https://api.openweathermap.org/data/2.5/weather?q=" + location + "&appid=" + "02c4be5475cd1da1275c305e6778a272"
                    api_link = requests.get(complete_api_link)
                    api_data = api_link.json()
                    current_temperature = int((api_data['main']["temp"]) - 273.15)
                    print(" The current temprature in " + location + " is " + format(
                        current_temperature) + " Degree Celsius")
                    speak(" The current temprature in " + location + "is" + format(
                        current_temperature) + "Degree Celsius")
                    print(complete_api_link)
                except:
                    print("sorry")
            else:
                print("please say clearly")


        elif "weather" in query:
            speak("whats the city name")
            location = takecommand()
            complete_api_link = "https://api.openweathermap.org/data/2.5/weather?q=" + location + "&appid=" + "02c4be5475cd1da1275c305e6778a272"
            api_link = requests.get(complete_api_link)
            api_data = api_link.json()
            current_temperature = int((api_data['main']["temp"]) - 273.15)
            weather_desc = api_data['weather'][0]['description']
            print(" Right now in " + location + " its " + format(current_temperature) + " Degrees , " + weather_desc)
            speak(" Right now in " + location + " its " + format(current_temperature) + " Degrees and " + weather_desc)
            print(complete_api_link)

        ############ Translator
        elif "translate" in query:
            print("What do you want to translate?")
            speak("What do you want to translate?")

            sentence = takecommand()
            if sentence == "None":
                speak("I couldn't hear you, please try again.")
                continue

            print("Which language to translate to?")
            speak("Which language to translate to?")
            ln = takecommand().lower()

            # Check if the language entered is in the LANGUAGES dictionary
            if ln in LANGUAGES.values():
                # Get the corresponding language code from the dictionary
                dest_language_code = [code for code, lang in LANGUAGES.items() if lang.lower() == ln][0]
                result = translate_text(sentence, dest_language_code)

                if result is None:
                    speak(f"Sorry, I couldn't translate to {ln}.")
                else:
                    print(f"In {ln.capitalize()}, you would say: {result}")
                    speak(f"In {ln.capitalize()}, you would say: {result}")
            else:
                print(f"Sorry, I don't support {ln}.")
                speak(f"Sorry, I don't support {ln}.")

        ####### TO DO
        elif 'add' in query:
            speak("What do you want to add?")
            item = takecommand()
            ToDo.toDoList(item)
            speak("Alright, I added to your list")

        elif 'show' in query or  'my list' in query:
            items = ToDo.showtoDoList()
            if len(items) == 1:
                speak(items[0])
                print(items[0])
            print('/n'.join(items))

        ######## Volume Control
        elif 'volume' in query:
            appControl.volumeControl(query)
            print('Volume Settings Changed')
            speak('Volume Settings Changed')  


        ######### NEWS Headlines
        elif isContain(query, ['news']):
            speak('Getting the latest news...')
            headlines, headlineLinks = webScrapping.latestNews(3)
            for head in headlines: print(head),speak(head)
            print('Do you want to read the full news?')
            speak('Do you want to read the full news?')
            text = takecommand()
            if isContain(text, ["no", "don't" ,"not now"]):
                print("No Problem " + ownerDesignation)
                speak("No Problem " + ownerDesignation)
            else:
                speak("Ok " + ownerDesignation + ", Opening browser...")
                webScrapping.openWebsite('https://indianexpress.com/latest-news/')
                print("You can now read the full news from this website.")
                speak("You can now read the full news from this website.")  
                break    


        ############# EXIT
        elif 'thankyou' in query or 'thanks' in query or 'thank you' in query or 'exit' in query or 'stop' in query:
            break

        elif "goodbye" in query or "offline" in query:
            print("Alright , going offline. It was nice working with you")
            speak("Alright , going offline. It was nice working with you")
            break

        elif 'stop' in query or "exit" in query or " bye" in query:
            print("Your personal AI assistant Taraa is turning off, good bye")
            speak("Your personal AI assistant Taraa is turning off, good bye")
            break


        ############# Respond with Normal Chat      
        else:
            result = normalChat.reply(query)
            if result != "None":
                speak(result)


