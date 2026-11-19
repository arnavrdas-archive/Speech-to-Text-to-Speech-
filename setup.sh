#!/bin/bash
echo "Setting up Speech-to-Text App..."
echo "Installing system dependencies..."
sudo apt update
sudo apt install python3-venv python3-pip portaudio19-dev -y

echo "Creating virtual environment..."
python3 -m venv venv

echo "Activating virtual environment..."
source venv/bin/activate

echo "Installing Python packages..."
pip install SpeechRecognition pyttsx3 pyaudio

echo "Setup complete! Run the app with:"
echo "source venv/bin/activate"
echo "python speech_app.py"