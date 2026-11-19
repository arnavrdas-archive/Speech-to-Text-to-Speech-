import tkinter as tk
from tkinter import scrolledtext, messagebox
import threading

try:
    import speech_recognition as sr
    import pyttsx3
    SPEECH_AVAILABLE = True
except ImportError:
    SPEECH_AVAILABLE = False

class SimpleSpeechApp:

    def __init__(self, root):
        self.root = root
        self.root.title("Speech-to-Text -> Text-to-Speech")
        self.root.geometry("500x400")
        
        self.setup_ui()
        
        if SPEECH_AVAILABLE:
            self.setup_speech()
        else:
            messagebox.showerror("Error", 
                "Required packages not installed.\n"
                "Run: pip install SpeechRecognition pyttsx3")
    
    def setup_ui(self):
        # Title
        # tk.Label(self.root, text="Speech-to-Text -> Text-to-Speech", 
        #         font=("Arial", 14, "bold")).pack(pady=10)
        
        # Record Button
        self.record_btn = tk.Button(self.root, text="Click to Record",
                                   command=self.record_audio,
                                   height=2, width=20, bg="#4CAF50", fg="white")
        self.record_btn.pack(pady=10)
        
        # Text Area
        tk.Label(self.root, text="Transcript (edit below):").pack()
        self.text_area = scrolledtext.ScrolledText(self.root, height=10, width=50)
        self.text_area.pack(pady=10, padx=20)
        
        # Play Button
        self.play_btn = tk.Button(self.root, text="Play as Speech",
                                 command=self.play_speech,
                                 height=2, width=20, bg="#2196F3", fg="white")
        self.play_btn.pack(pady=10)
        
        # Status Label
        self.status = tk.Label(self.root, text="Ready", fg="gray")
        self.status.pack()
    
    def setup_speech(self):
        try:
            self.recognizer = sr.Recognizer()
            self.tts = pyttsx3.init()
            # Optional: Set speech rate
            self.tts.setProperty('rate', 75)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to initialize speech: {e}")
    
    def record_audio(self):
        if not SPEECH_AVAILABLE:
            messagebox.showerror("Error", "Speech recognition not available")
            return
            
        self.record_btn.config(state="disabled", text="Listening...")
        self.status.config(text="Speak now...", fg="blue")
        
        # Run in thread to avoid freezing UI
        thread = threading.Thread(target=self._record_audio)
        thread.daemon = True
        thread.start()
    
    def _record_audio(self):
        try:
            with sr.Microphone() as source:
                self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
                audio = self.recognizer.listen(source, timeout=5)
                
                text = self.recognizer.recognize_google(audio)
                
                # Update UI from main thread
                self.root.after(0, self.update_text, text)
                self.root.after(0, lambda: self.status.config(
                    text="Success!", fg="green"))
                
        except sr.WaitTimeoutError:
            self.root.after(0, lambda: self.status.config(
                text="No speech detected", fg="red"))
        except sr.UnknownValueError:
            self.root.after(0, lambda: self.status.config(
                text="Could not understand", fg="red"))
        except Exception as e:
            self.root.after(0, lambda: self.status.config(
                text=f"Error: {e}", fg="red"))
        finally:
            self.root.after(0, lambda: self.record_btn.config(
                state="normal", text="Click to Record"))
    
    def update_text(self, text):
        self.text_area.delete(1.0, tk.END)
        self.text_area.insert(1.0, text)
    
    def play_speech(self):
        if not SPEECH_AVAILABLE:
            messagebox.showerror("Error", "Text-to-speech not available")
            return
            
        text = self.text_area.get(1.0, tk.END).strip()
        if not text:
            self.status.config(text="No text to speak", fg="red")
            return
            
        self.play_btn.config(state="disabled")
        self.status.config(text="Speaking...", fg="blue")
        
        # Run in thread
        thread = threading.Thread(target=self._play_speech, args=(text,))
        thread.daemon = True
        thread.start()
    
    def _play_speech(self, text):
        try:
            self.tts.say(text)
            self.tts.runAndWait()
            self.root.after(1, lambda: self.status.config(
                text="Playback complete", fg="green"))
        except Exception as e:
            self.root.after(0, lambda: self.status.config(
                text=f"Playback error: {e}", fg="red"))
        finally:
            self.root.after(0, lambda: self.play_btn.config(state="normal"))

if __name__ == "__main__":
    root = tk.Tk()
    app = SimpleSpeechApp(root)
    root.mainloop()