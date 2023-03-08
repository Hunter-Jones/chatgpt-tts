# Make sure to set OPENAI_API_KEY at https://platform.openai.com/account/api-keys

# OpenAI setup
import openai
import speech_recognition

openai.api_key = ""
openai.Model.list()

# Text to speech setup
import speech_recognition as sr
import pyttsx3
engine = pyttsx3.init()
my_mic = sr.Microphone()
r = sr.Recognizer()


# Requires a text message (ex "tell me a joke") which is then sent to chatgpt
# Note it will often cause errors because gpt sometimes cant take requests
# It will then return the chatgpt response
def gpt_request(message):
    completion = ""
    try:
        completion = openai.ChatCompletion.create(
          model="gpt-3.5-turbo",
          messages=[
            {"role": "user", "content": message}
          ]
        )

    except:
        print_and_say("It appears there is an issue with chatgpt at the moment")
    return completion.choices[0].message.content


# Input Requires nothing
# Output Using the microphone, this function reads in a response to speech using the google voice recognition software
# and then returns the tts output of the microphone as a string
def get_mic_input():
    with my_mic as source:
        r.adjust_for_ambient_noise(source)
        audio = r.listen(source)
        response = ""

        try:
            response = r.recognize_google(audio)

        except speech_recognition.UnknownValueError:
            print_and_say("Sorry I wasn't sure what you said. Please say wake up, help me, or goodbye")

        except speech_recognition.RequestError:
            print_and_say("If you aren't connected to WiFi, this application requires WiFi to work")
            print_and_say("Otherwise there was an issue reaching chatGPT servers")

        return response


# Inputs a message
# Outputs prints the message to both tts and cli
def print_and_say(message):
    print(message)
    engine.say(message)
    engine.runAndWait()


# Input requires nothing
# Output this function outputs to tts and cli rules for how to use the application
def help_command():
    print_and_say("Hello this is a text-to-speech chatgpt program.")
    print_and_say("To use please say the command 'wake up'")
    print_and_say("And then wait for the message saying 'Please say your chatgpt command' before responding with")
    print_and_say("You can also say goodbye or help me to end the program or hear the options again")
    print_and_say("Be prepared because it does take a couple seconds to process voice inputs")


help_command()
EXIT_FLAG = False
while not EXIT_FLAG:
    print("Listening For Response")
    user_input = get_mic_input()

    WAKE = "wake up"
    EXIT = "goodbye"
    HELP = "help me"
    if user_input.count(WAKE) > 0:
        print_and_say("Please say your chatgpt command")

        user_input = get_mic_input()
        print(user_input)
        print_and_say(gpt_request(user_input))

    if user_input.count(EXIT) > 0:
        print_and_say("Goodbye")
        EXIT_FLAG = True

    if user_input.count(HELP) > 0:
        help_command()