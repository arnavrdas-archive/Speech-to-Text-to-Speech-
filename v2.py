import tkinter as tk
# import speech_recognition as sr
import pyttsx3

root = tk.Tk()
root.title("Speech-to-Text -> Text-to-Speech")
root.geometry("400x300")

recognizer = sr.Recognizer()

engine = pyttsx3.init()
engine.setProperty('rate', 75)

def mic():
    status.config(text="Status: Mic Button was clicked!")

    with sr.Microphone() as source:

    print("Adjusting for ambient noise...")
    recognizer.adjust_for_ambient_noise(source, duration=1)

    print("Speak now:")
    audio = recognizer.listen(source, timeout=5, phrase_time_limit=10)

    try:
        text = recognizer.recognize_google(audio)
        status.config(text={text})
    except sr.UnknownValueError:
        print("Could not understand audio")
    except sr.RequestError as e:
        print(f"Service error: {e}")
    except sr.WaitTimeoutError:
        print("No speech detected")
    except Exception as e:
        print(f"Error: {e}")

def speak():

    status.config(text="Status: Speak Button was clicked!")

    engine.say("This text is spoken with custom rate, volume, and voice.")
    engine.runAndWait()

status = tk.Label(root, text="Status: Ready")
status.pack()

micButton = tk.Button(root, text="Mic", command=mic)
micButton.pack()

speakButton = tk.Button(root, text="Speaker", command=speak)
speakButton.pack()

# entry = tk.Entry(root).pack()

# button = tk.Button(root, text="Submit", command=get_text).pack()
# def get_text():
#     text = entry.get()
#     status.config(text=f"You entered: {text}")

root.mainloop()