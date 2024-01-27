import speech_recognition as sr
import win32com.client
import webbrowser
import openai
from config import apikey
import datetime
import random
import subprocess
from maintest import getjob

speaker = win32com.client.Dispatch("SAPI.SpVoice")
chatStr = ""


def chat(query):
    global chatStr
    print(chatStr)
    openai.api_key = apikey
    chatStr += f"Suprith: {query}\n Munki: "
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=chatStr,
        temperature=0.7,
        max_tokens=256,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    try:
        say(response["choices"][0]["text"])
        chatStr += f"{response['choices'][0]['text']}\n"
        return response["choices"][0]["text"]
    except:
        return "Something went wrong"


def ai(prompt):
    openai.api_key = apikey
    text = f"OpenAI response for Prompt: {prompt} \n *************************\n\n"

    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=prompt,
        temperature=0.7,
        max_tokens=256,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )

    text += response["choices"][0]["text"]
    # if not subprocess.path.exists("Openai"):
    #     # os.mkdir("Openai")
    #     subprocess.run(['mkdir', "openAI"], shell=True)

    # with open(f"Openai/prompt- {random.randint(1, 2343434356)}", "w") as f:
    with open(f"openAI/{''.join(prompt.split('intelligence')[1:]).strip()}.txt", "w") as f:
        f.write(text)


def say(text):
    speaker.Speak(text)


def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        # r.pause_threshold =  0.6
        audio = r.listen(source)
        try:
            print("Recognizing...")
            query = r.recognize_google(audio, language="en-in")
            print(f"User said: {query}")
            return query
        except Exception as e:
            return "Some Error Occurred. Sorry from Munki"


if __name__ == '__main__':
    print('Welcome')
    speaker.Speak("Im Munki AI, how can I help you?")
    while True:
        print("Listening...")
        query = takeCommand()

        sites = [["youtube", "https://www.youtube.com"], ["wikipedia", "https://www.wikipedia.com"],
                 ["google", "https://www.google.com"], ]
        for site in sites:
            if f"Open {site[0]}".lower() in query.lower():
                speaker.Speak(f"Opening {site[0]} sir...")
                webbrowser.open(site[1])

        if "open music" in query:
            musicPath = "C:/Users/supri/Music/TAketootherlevel/Gemtracks-Summer-Pride-779/Gemtracks-Summer-Pride.mp3"
            # os.system(f"open {musicPath}")

        elif "the time" in query:

            hour = datetime.datetime.now().strftime("%H")
            min = datetime.datetime.now().strftime("%M")
            say(f"Sir time is {hour}  {min} ")

        elif "open valorant".lower() in query.lower():
            subprocess.run(['explorer', f"open C:/Riot Games/Riot Client"])



        elif "Using artificial intelligence".lower() in query.lower():
            ai(prompt=query)

        elif "search jobs" in query.lower():
            say("What company do you wanna apply for?")
            queryJ = takeCommand()
            if "amd" in queryJ.lower():
                openings = getjob()
                for i in range(5):
                    say(openings[i])

        elif "Quit".lower() in query.lower():
            exit()

        elif "reset chat".lower() in query.lower():
            chatStr = ""

        else:
            say("Do you wanna chat with GPT?")
            if "yes" in takeCommand().lower():
                say("Go ahead, ask your question")
                print("Chatting...")
                chat(query)
            else:
                exit()