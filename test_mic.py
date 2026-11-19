import speech_recognition as sr

r = sr.Recognizer()
with sr.Microphone() as source:
    print("Adjusting for noise...")
    r.adjust_for_ambient_noise(source, duration=1)
    print("Speak something...")
    audio = r.listen(source)
    
try:
    text = r.recognize_google(audio)
    print(f"You said: {text}")
except Exception as e:
    print(f"Error: {e}")